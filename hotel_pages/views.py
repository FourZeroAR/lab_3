import plotly.express as px
from plotly.offline import plot
from django.shortcuts import render, get_object_or_404, redirect
from hotel.models import Booking, Room, Guest
from .analytics import HotelAnalytics
from .forms import BookingForm
from .NetworkHelper import NetworkHelper
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import cumsum
from bokeh import __version__ as bokeh_version
from math import pi
import time
from concurrent.futures import ThreadPoolExecutor

def booking_list(request):
    bookings = Booking.objects.all().select_related('room', 'guest')
    return render(request, 'hotel_pages/booking_list.html', {'bookings': bookings})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'hotel_pages/booking_detail.html', {'booking': booking})

def booking_edit(request, pk=None):
    if pk:
        booking = get_object_or_404(Booking, pk=pk)
    else:
        booking = Booking()
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'hotel_pages/booking_form.html', {'form': form})


def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        booking.delete()
        return redirect('booking_list')
    return render(request, 'hotel_pages/booking_confirm_delete.html', {'booking': booking})

def colleague_books(request):
    books = NetworkHelper.get_books()
    return render(request, 'hotel_pages/colleague_books.html', {'books': books})


def colleague_book_delete(request, pk):
    if request.method == "POST":
        NetworkHelper.delete_book(pk)
    return redirect('colleague_books')


# --- DASHBOARD V1 (Plotly) ---

def dashboard_v1(request):
    analytics = HotelAnalytics()

    stats_df = analytics.get_descriptive_statistics()
    stats_html = stats_df.to_html(classes='dataframe', border=0)

    def style_plotly(fig):
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="#2c3034", plot_bgcolor="#2c3034",
            font=dict(color="#e9ecef"), margin=dict(l=60, r=40, t=80, b=60)
        )
        return fig

    fig1 = style_plotly(
        px.bar(analytics.get_df_revenue_by_type(), x='type', y='total_revenue', title="Revenue Analysis", color='type'))
    df_pop = analytics.get_df_room_popularity().sort_values('count', ascending=False).head(10)
    fig2 = style_plotly(px.pie(df_pop, names='number', values='count', title="Top 10 Popular Rooms"))
    fig3 = style_plotly(
        px.line(analytics.get_df_monthly_dynamics(), x='month', y='count', title="Monthly Dynamics", markers=True))

    df_status = analytics.get_df_occupancy_status()
    df_status['status'] = df_status['is_booked'].map({True: 'Occupied', False: 'Free'})
    fig4 = style_plotly(px.pie(
        df_status, names='status', values='count', title="Room Status",
        color='status', color_discrete_map={'Occupied': '#dc3545', 'Free': '#198754'}
    ))

    fig5 = style_plotly(
        px.bar(analytics.get_df_vip_guests(), y='guest_name', x='total_spent', orientation='h', title="Top VIP Guests"))
    fig6 = style_plotly(px.scatter(analytics.get_df_price_efficiency(), x='bookings_count', y='avg_check',
                                   size='avg_check', color='room_number', hover_name='room_number',
                                   title="Price Efficiency"))

    graphs_html = [plot(f, output_type='div', include_plotlyjs=(i == 0)) for i, f in
                   enumerate([fig1, fig2, fig3, fig4, fig5, fig6])]

    return render(request, 'hotel_pages/dashboard_v1.html', {
        'graphs': graphs_html,
        'pandas_stats': stats_html
    })


# --- DASHBOARD V2 (Bokeh) ---

def dashboard_v2(request):
    analytics = HotelAnalytics()

    stats_df = analytics.get_descriptive_statistics()
    stats_html = stats_df.to_html(classes='dataframe', border=0)

    def apply_minimal_theme(p):
        p.background_fill_color = "#2c3034";
        p.border_fill_color = "#2c3034";
        p.title.text_color = "#0dcaf0"
        p.xaxis.axis_label_text_color = "white";
        p.yaxis.axis_label_text_color = "white"
        p.xaxis.major_label_text_color = "#adb5bd";
        p.yaxis.major_label_text_color = "#adb5bd"
        if p.legend:
            p.legend.background_fill_color = "#343a40"
            p.legend.label_text_color = "white"
        return p

    df_rev = analytics.get_df_revenue_by_type()
    p1 = figure(x_range=list(df_rev['type']), height=320, title="Revenue Analysis", toolbar_location=None)
    p1.vbar(x='type', top='total_revenue', width=0.8, color="#0dcaf0", source=ColumnDataSource(df_rev))
    apply_minimal_theme(p1)

    df_pop = analytics.get_df_room_popularity().sort_values('count', ascending=False).head(10)
    df_pop['angle'] = df_pop['count'] / df_pop['count'].sum() * 2 * pi
    colors = ['#0dcaf0', '#6610f2', '#6f42c1', '#d63384', '#fd7e14', '#198754', '#ffc107', '#20c997', '#e83e8c',
              '#6c757d']
    df_pop['color'] = colors[:len(df_pop)]
    p2 = figure(height=320, title="Top 10 Popular Rooms", toolbar_location=None, x_range=(-0.5, 1.8))
    p2.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True),
             end_angle=cumsum('angle'), line_color="#2c3034", fill_color='color', legend_field='number', source=df_pop)
    apply_minimal_theme(p2)

    df_month = analytics.get_df_monthly_dynamics()
    p3 = figure(height=320, title="Monthly Dynamics")
    p3.line(df_month['month'], df_month['count'], line_width=3, color="#0dcaf0")
    apply_minimal_theme(p3)

    df_occ = analytics.get_df_occupancy_status()
    df_occ['status'] = df_occ['is_booked'].map({True: 'Occupied', False: 'Free'})
    df_occ['color'] = df_occ['status'].map({'Occupied': '#dc3545', 'Free': '#198754'})
    df_occ['angle'] = df_occ['count'] / df_occ['count'].sum() * 2 * pi
    p4 = figure(height=320, title="Occupancy Status", toolbar_location=None, x_range=(-0.5, 1.2))
    p4.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True),
             end_angle=cumsum('angle'), line_color="#2c3034", fill_color='color', legend_field='status', source=df_occ)
    apply_minimal_theme(p4)

    df_vip = analytics.get_df_vip_guests()
    p5 = figure(y_range=list(df_vip['guest_name']), height=320, title="Top VIP Guests")
    p5.hbar(y='guest_name', right='total_spent', height=0.6, color="#6610f2", source=ColumnDataSource(df_vip))
    apply_minimal_theme(p5)

    df_eff = analytics.get_df_price_efficiency()
    p6 = figure(height=320, title="Price Efficiency (Hover for Info)")
    p6.scatter('bookings_count', 'avg_check', size=15, color="#fd7e14", alpha=0.6, source=ColumnDataSource(df_eff))
    p6.add_tools(HoverTool(tooltips=[("Room", "@room_number"), ("Avg Check", "$@avg_check")]))
    apply_minimal_theme(p6)

    script, divs = components({'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5, 'p6': p6})

    return render(request, 'hotel_pages/dashboard_v2.html', {
        'script': script, 'divs': divs, 'bokeh_version': bokeh_version,
        'pandas_stats': stats_html
    })

# --- PERFORMANCE TEST ---

def heavy_database_task():
    return list(Booking.objects.all().select_related('room', 'guest'))

def performance_test(request):
    total_requests = 100
    thread_settings = [1, 2, 4, 8, 16, 32]
    results = []

    for num_threads in thread_settings:
        start_time = time.time()

        if num_threads == 1:
            for _ in range(total_requests):
                heavy_database_task()
        else:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                list(executor.map(lambda _: heavy_database_task(), range(total_requests)))

        end_time = time.time()
        results.append(round(end_time - start_time, 4))

    sync_time = results[0]
    best_para_time = min(results)
    speedup = round(sync_time / best_para_time, 2)

    context = {
        'sync_time': sync_time,
        'para_time': best_para_time,
        'speedup': speedup,
        'thread_counts': thread_settings,
        'execution_times': results,
    }

    return render(request, 'hotel_pages/performance.html', context)