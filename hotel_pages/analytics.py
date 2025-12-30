import pandas as pd
from hotel.models import Booking, Room

class HotelAnalytics:
    def get_df_bookings(self):
        bookings = Booking.objects.all().select_related('room', 'guest')
        data = []
        for b in bookings:
            data.append({
                'id': b.id,
                'room_number': b.room.number,
                'type': b.room.room_type,
                'price': b.room.price,
                'guest_name': b.guest.name,
                'check_in': b.check_in,
                'total_revenue': b.total if b.total else 0,
                'month': b.check_in.month if b.check_in else 1
            })
        return pd.DataFrame(data)

    def get_descriptive_statistics(self):
        df = self.get_df_bookings()
        if df.empty:
            return pd.DataFrame(columns=['price', 'total_revenue'])
        return df[['price', 'total_revenue']].describe()

    def get_df_revenue_by_type(self):
        df = self.get_df_bookings()
        if df.empty: return pd.DataFrame(columns=['type', 'total_revenue'])
        return df.groupby('type')['total_revenue'].sum().reset_index()

    def get_df_room_popularity(self):
        df = self.get_df_bookings()
        if df.empty: return pd.DataFrame(columns=['room_number', 'count'])
        return df.groupby('room_number').size().reset_index(name='count').rename(columns={'room_number': 'number'})

    def get_df_monthly_dynamics(self):
        df = self.get_df_bookings()
        if df.empty: return pd.DataFrame(columns=['month', 'count'])
        return df.groupby('month').size().reset_index(name='count').sort_values('month')

    def get_df_occupancy_status(self):
        rooms = Room.objects.all()
        data = [{'is_booked': r.is_booked} for r in rooms]
        df = pd.DataFrame(data)
        if df.empty: return pd.DataFrame(columns=['is_booked', 'count'])
        return df.groupby('is_booked').size().reset_index(name='count')

    def get_df_vip_guests(self):
        df = self.get_df_bookings()
        if df.empty: return pd.DataFrame(columns=['guest_name', 'total_spent'])
        vip = df.groupby('guest_name')['total_revenue'].sum().reset_index(name='total_spent')
        return vip.sort_values('total_spent', ascending=False).head(5)

    def get_df_price_efficiency(self):
        df = self.get_df_bookings()
        if df.empty: return pd.DataFrame(columns=['room_number', 'bookings_count', 'avg_check'])
        eff = df.groupby('room_number').agg({'id': 'count', 'total_revenue': 'mean'}).reset_index()
        eff.columns = ['room_number', 'bookings_count', 'avg_check']
        return eff