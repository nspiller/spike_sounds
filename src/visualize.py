import matplotlib.pylab as plt
import numpy as np
import io
import imageio

from joblib import Parallel, delayed, parallel_backend

def plot_data(
    data,
    key_vlines=[],
    t_cutoff=None,
    xlims=(None, None),
    xlabel="time [s]",
    linewidth=0.5,
    linelengths=1,
    figsize=(10, 5),
    palette="tab10",
    palette_vlines="Pastel1",
):
    fig, ax = plt.subplots(figsize=figsize)

    cmap = plt.get_cmap(palette)
    cmap_vlines = plt.get_cmap(palette_vlines)

    i, j = 0, 0
    ylabels = []

    for name in data:
        time_events = data[name]
        if t_cutoff is not None:
            mask = time_events < t_cutoff
            time_events = time_events[mask]

        if name in key_vlines:
            label = name
            for t in time_events:
                ax.axvline(
                    t, color=cmap_vlines(j % cmap_vlines.N), label=label, zorder=99
                )
                label = None
            j += 1
        else:
            ax.eventplot(
                time_events,
                lineoffsets=i,
                linewidth=linewidth,
                linelengths=linelengths,
                colors=cmap(i % cmap.N),
            )
            i += 1
            ylabels.append(name)

    ax.set_xlim(xlims)
    ax.set_xlabel(xlabel)
    ax.set_ylim(-0.5, len(ylabels) - 0.5)

    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels)
    if j:
        ax.legend(loc="upper right")

    return fig, ax


def hide_axes_and_legend(ax):
    """Remove ticks and labels from axes for cleaner plots.

    Parameters
    ----------
    ax : axes object
        Axes with ticks and labels to be removed.
    """

    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_yticklabels([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_axis_off()


def draw_time_indicator(ax, time_point, color="red"):
    ax.axvline(time_point, color=color, zorder=99)


def convert_figure_to_image(fig, dpi):
    buffer = io.BytesIO()
    fig.savefig(buffer, dpi=dpi)

    frame = imageio.imread(buffer)

    return frame


def draw_frame(data, time_point, t_max, plot_params, dpi, matplotlib_style):
    with plt.style.context(matplotlib_style):
        fig, ax = plot_data(data, t_cutoff=time_point, xlims=(0, t_max), **plot_params)

        draw_time_indicator(ax, time_point=time_point)
        hide_axes_and_legend(ax)

        frame = convert_figure_to_image(fig, dpi=dpi)
        plt.close(fig)

        return frame


def generate_movie(
    data, time_resolution, plot_params, path_movie, dpi=300, matplotlib_style="classic"
):
    t_max = np.concatenate([*data.values()]).max()
    time_points = np.arange(0, t_max, time_resolution)

    with parallel_backend("loky", n_jobs=-1):
        frames = Parallel()(
            delayed(draw_frame)(data, t, t_max, plot_params, dpi, matplotlib_style)
            for t in time_points
        )

    with imageio.get_writer(
        path_movie, format="FFMPEG", fps=1 / time_resolution
    ) as writer:
        for frame in frames:
            writer.append_data(frame)
