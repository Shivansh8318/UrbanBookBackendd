import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import AvailabilitySlot, Booking
from teacher.models import Teacher  # Import Teacher model

class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'booking_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'add_slot':
            await self.add_slot(data)
        elif action == 'book_slot':
            await self.book_slot(data)

    async def add_slot(self, data):
        teacher_user_id = data.get('teacher_id')  # This is the user_id (string)
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Fetch the Teacher object using user_id
        teacher = await database_sync_to_async(Teacher.objects.get)(user_id=teacher_user_id)

        # Create the AvailabilitySlot using the Teacher object
        slot = await database_sync_to_async(AvailabilitySlot.objects.create)(
            teacher=teacher,  # Pass the Teacher object directly
            date=date,
            start_time=start_time,
            end_time=end_time,
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'slot_update',
                'slot': {
                    'id': slot.id,
                    'teacher_id': slot.teacher_id,
                    'date': str(slot.date),
                    'start_time': str(slot.start_time),
                    'end_time': str(slot.end_time),
                    'is_booked': slot.is_booked,
                }
            }
        )

    async def book_slot(self, data):
        slot_id = data.get('slot_id')
        student_id = data.get('student_id')

        slot = await database_sync_to_async(AvailabilitySlot.objects.get)(id=slot_id)
        slot.is_booked = True
        await database_sync_to_async(slot.save)()

        booking = await database_sync_to_async(Booking.objects.create)(
            slot=slot,
            student_id=student_id,
            status='pending'
        )

        await self.channel_layer.group_send(
            f'booking_{slot.teacher_id}',
            {
                'type': 'booking_update',
                'booking': {
                    'id': booking.id,
                    'slot_id': slot.id,
                    'student_id': student_id,
                    'status': booking.status,
                }
            }
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'booking_update',
                'booking': {
                    'id': booking.id,
                    'slot_id': slot.id,
                    'student_id': student_id,
                    'status': booking.status,
                }
            }
        )

    async def slot_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'slot_update',
            'slot': event['slot']
        }))

    async def booking_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'booking_update',
            'booking': event['booking']
        }))