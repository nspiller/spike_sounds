import matplotlib.pylab as plt

def plot_data(data, vline_keys=[], save_path=''):


    fig, ax = plt.subplots()

    lineoffset = 0
    vline_color_id = 1
    for key, time_events in data.items():

        if key in vline_keys:
            for t in time_events:
                ax.axvline(t, color=f'C{vline_color_id}', label=key)
            vline_color_id += 1

        else:
            ax.eventplot(time_events, lineoffsets=lineoffset, color='C0')
            lineoffset += 1

    # legend
    h, l = ax.get_legend_handles_labels()
    if h:
        ax.legend((h[0], h[-1]), (l[0], l[-1]), loc='upper left', bbox_to_anchor=(1., 1))

    ax.set_xlabel('time')
    ax.set_yticklabels([])
    ax.set_yticks(range(lineoffset))

    # optional: save to file and close
    if save_path:
        fig.savefig(save_path)
        plt.close(fig)