import matplotlib.pylab as plt
import numpy as np
import io
import imageio

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



def plot_frame(l_time_events, time_interval, time_point):

    fig, ax = plt.subplots()

    for i, time_events in enumerate(l_time_events):

        mask = time_events < time_point
        ax.eventplot(time_events[mask], lineoffsets=i, colors=f'C{i}')
    
    ax.axvline(time_point, color='gray')

    ax.set_xlim(time_interval)
    ax.set_ylim(-.5, len(l_time_events) - .5)

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
 
    
def generate_movie(l_time_events, time_interval, time_resolution, path_movie):

    time_points = np.arange(*time_interval, time_resolution)

    frames = []
    for time_point in time_points:
        fig = plot_frame(l_time_events, time_interval, time_point)
        frames.append(convert_figure_to_image(fig))
        plt.close(fig)

    with imageio.get_writer(path_movie, format='FFMPEG', fps=1 / time_resolution) as writer:
        for frame in frames:
            writer.append_data(frame)