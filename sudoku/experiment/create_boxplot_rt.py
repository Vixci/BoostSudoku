import argparse
import pandas
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def get_category_order_labels(category_order, attribute, strategy, row):
    """ Hand-crafted category order and corresponding labels for x-axis in box plots """

    labels = []
    if attribute == "initial_clauses":
            category_order =['>25','22-25','19-21','<19']
            # category_order =['>25','<25']
            labels = ['Easy','Medium','Hard','Very hard']
    else:
        labels = category_order

    # no labels for top row
    if row == 0:
        labels = []
        for n in range(len(category_order)):
            labels.append('')

    return category_order, labels


if __name__ == '__main__':

    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, required=True, help="csvs, comma separated")
    parser.add_argument('--output_folder', type=str, required=True, help="name of output folder")
    args, _ = parser.parse_known_args()

    # determine which attributes to plot
    attributes = ['initial_clauses']

    # load input CSVs
    csvs = []
    for input_file in args.csv.split(","):
        csvs.append(pandas.read_csv(input_file))
    all_data = pandas.concat(csvs)
    print(all_data)
    #all_data['initial_clauses'] = np.where(all_data.initial_clauses > 25, '>25', '<25')

    difficult = lambda t: '>25' if t > 25 else ('22-25' if t >= 22 else ('19-21' if t >=19 else '<19'))
    all_data['initial_clauses'] = np.array([difficult(xi) for xi in all_data['initial_clauses']])
    # print(all_data['initial_clauses'])

    # create output folder
    output_folder = args.output_folder
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    # set datasets
    datasets = ["4", "9"]
    dataset_labels = ["SUDOKU4", "SUDOKU9"]

    # set strategy
    strategies = all_data.strategy.unique()

    print(strategies)

    # set metric label
    metric_label = "Runtime"

    # order and label for strategies
    # strategy_order = ['0', '1', '2', '3', '4']
    strategy_order = [0,1,2,3,4]
    strategy_labels = ['Basic',
            'DCLS',
            'DLIS',
            'JW-OS',
            'JW-TS',
            ]

    print("Plotting metric per strategy...")
    f, axes = plt.subplots(1, len(datasets), sharex=True, sharey=True)
    f.set_size_inches(6.4, 2.4)
    plt.subplots_adjust(hspace=0.2, wspace=0.1)
    font_size = 7.5
    label_rotation=15
    for i in range(len(datasets)):
        current_dataset = int(datasets[i])
        title = dataset_labels[i]
        print(current_dataset)
        print(all_data['sudoku_size'])
        # get data for current dataset
        dataset_data = all_data[all_data.sudoku_size == current_dataset]
        print(dataset_data)

        # create plots
        runtime_per_strategy = sns.boxplot(y=dataset_data['runtime']*100,
                x=dataset_data['strategy'],
                order=strategy_order,
                linewidth=0.5,
                fliersize=1,
                width=0.8,
                ax=axes[i])
        runtime_per_strategy.set_title(title, size=font_size)
        runtime_per_strategy.tick_params(labelsize=font_size)
        if i == 0:
            runtime_per_strategy.set_ylabel(metric_label, fontsize=font_size)
        else:
            runtime_per_strategy.set_ylabel('')

    for ax in axes.flat:
        ax.set_xticklabels(strategy_labels)
        ax.set(xlabel='')

    # save figure
    runtime_per_strategy.get_figure().savefig(
            output_folder + '/runtime_per_strategy.pdf',
            dpi=300,
            bbox_inches='tight',
            pad_inches=0)

    # plot each attribute vs metric
    for attribute in attributes:
        attribute_name = attribute
        print("Plotting {}...".format(attribute_name))

        # create plot
        label_rotation=30
        font_size = 7.5
        num_rows = len(datasets)
        num_cols = len(strategies)


        f, axes = plt.subplots(num_rows, num_cols, sharex=True, sharey=True)
        if attribute == "initial_clauses":
            f.set_size_inches(6, 4)
        plt.subplots_adjust(hspace=0.1, wspace=0.2)
        plt.xticks(rotation=label_rotation)

        # add dataset names to subplot rows
        row_names = ["SUDOKU4", "SUDOKU9"]
        pad = 5
        for ax, row in zip(axes[:,0], row_names):
            ax.annotate(row, xy=(0, 0.5), rotation=90, xytext=(-ax.yaxis.labelpad - pad, 0),
                        xycoords=ax.yaxis.label, textcoords='offset points',
                        size=font_size, ha='right', va='center')

        # each strategy is a column in the main plot
        for col in range(len(strategy_order)):
            current_strategy = strategy_order[col]
            title = strategy_labels[col]

            # get data for current strategy
            strategy_data = all_data[all_data.strategy == current_strategy]
            print(strategy_data)

            # each dataset is a row in the main plot
            for row in range(len(datasets)):
                current_dataset = int(datasets[row])

                # set order and labels for categories in x axis of box plot
                category_order = sorted(strategy_data[attribute].fillna(0).unique())
                category_order, labels = get_category_order_labels(category_order, attribute, current_strategy, row)
                if attribute == "initial_clauses":
                    global_legends = labels
                    labels = ['', '', '', '']

                dataset_data = strategy_data.loc[strategy_data['sudoku_size'] == current_dataset]
                if attribute == "initial_clauses":
                    colors=sns.color_palette()
                    box = sns.boxplot(x=dataset_data[attribute],
                            y=dataset_data['runtime']*100,
                            order=category_order,
                            linewidth=0.5,
                            fliersize=1,
                            palette=colors,
                            ax=axes[row][col]
                            )
                else:
                    box = sns.boxplot(x=dataset_data[attribute],
                            y=dataset_data['runtime']*100,
                            order=category_order,
                            linewidth=0.5,
                            fliersize=1,
                            ax=axes[row][col]
                            )

                if row != len(datasets) - 1:
                    box.set_title(title, size=font_size)
                box.tick_params(labelsize=font_size)
                if col == 0:
                    box.set_ylabel(metric_label, fontsize=font_size)
                else:
                    box.set_ylabel('')

                # add xticks labels
                axes[row][col].set_xticklabels(labels, ha='right')

        # add labels to box plots
        for ax in axes.flat:
            plt.sca(ax)
            plt.xticks(rotation=label_rotation)
            ax.set(xlabel='')

        # add legend
        if attribute == "initial_clauses":
            proxies = []
            for i in range(len(global_legends)):
                proxies.append(plt.Rectangle(
                    (0,0),
                    1,
                    1,
                    ec='k',
                    fc=colors[i],
                    linewidth=0.5,
                    label=global_legends[i]))
            f.legend(
                    prop={'size': 5.5},
                    handles=proxies,
                    bbox_to_anchor=(0.01, 0.02),
                    loc='lower left',
                    borderaxespad=0.,
                    columnspacing=1,
                    ncol=7,
                    frameon=False,
                    )

        # save figure for current attribute
        box.get_figure().savefig(
                output_folder + '/' + attribute_name + '.pdf',
                dpi=300,
                bbox_inches='tight',
                pad_inches=0)

    print('DONE! Find plots in folder:', output_folder)
