import matplotlib.pylab as plt
import numpy as np
import io
import imageio

def plot_data(data, vline_keys=[], linewidth=.5, linelengths=1, figsize=(10, 5), save_path=''):


    fig, ax = plt.subplots(figsize=figsize)

    lineoffset = 0
    vline_color_id = 1
    for key, time_events in data.items():

        if key in vline_keys:
            for t in time_events:
                ax.axvline(t, color=f'C{vline_color_id}', label=key)
            vline_color_id += 1

        else:
            ax.eventplot(time_events, lineoffsets=lineoffset, linewidth=linewidth, linelengths=linelengths, color='C0')
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



def plot_frame(l_time_events, time_point=None, hide_axes=False, xlims=(None, None), linewidth=.5, linelengths=1, figsize=(10, 5),):

    fig, ax = plt.subplots(figsize=figsize)

    for i, time_events in enumerate(l_time_events):

        if time_point is not None:
            mask = time_events < time_point
            time_events = time_events[mask]
            ax.axvline(time_point, color='red', zorder=99)

        ax.eventplot(time_events, lineoffsets=i, linewidth=linewidth, linelengths=linelengths, colors=f'C{i}')
    
    ax.set_xlim(xlims)
    ax.set_ylim(-.5, len(l_time_events) - .5)

    if hide_axes:
        ax.set_xticklabels([])
        ax.set_xticks([])
        ax.set_yticklabels([])
        ax.set_yticks([])

    return fig

def convert_figure_to_image(fig):

    buffer = io.BytesIO()
    fig.savefig(buffer)

    frame = imageio.imread(buffer)

    return frame
 
    
def generate_movie(l_time_events, time_resolution, plot_params, path_movie):

    
    t_max = np.concatenate(l_time_events).max()
    time_points = np.arange(0, t_max, time_resolution)

    frames = []
    for time_point in time_points:
        fig = plot_frame(l_time_events, time_point, xlims=(0, t_max), **plot_params)
        frames.append(convert_figure_to_image(fig))
        plt.close(fig)

    with imageio.get_writer(path_movie, format='FFMPEG', fps=1 / time_resolution) as writer:
        for frame in frames:
            writer.append_data(frame)