# core/ws_manager.py
import json
import uuid

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        # {user_id: websocket} para cada canal
        self.stock: dict[str, WebSocket] = {}
        self.chat: dict[str, WebSocket] = {}
        self.presence: dict[str, WebSocket] = {}

    # ──────────────────────────── Conexión ────────────────────────────

    async def connect(self, channel: str, user_id: str, websocket: WebSocket):
        """Acepta la conexión y la registra en el canal correspondiente."""
        await websocket.accept()
        getattr(self, channel)[user_id] = websocket

        # notificar a todos que este usuario está online
        await self.broadcast_presence(user_id, status="online")

    async def disconnect(self, channel: str, user_id: str):
        """Elimina la conexión del canal y notifica que el usuario se fue."""
        channel_dict: dict = getattr(self, channel)
        if user_id in channel_dict:
            del channel_dict[user_id]

        # notificar solo si el usuario no tiene conexiones en ningún canal
        if not self._user_is_connected(user_id):
            await self.broadcast_presence(user_id, status="offline")

    def _user_is_connected(self, user_id: str) -> bool:
        """Verifica si el usuario tiene al menos una conexión activa."""
        return (
            user_id in self.stock or
            user_id in self.chat or
            user_id in self.presence
        )

    # ──────────────────────────── Stock ────────────────────────────

    async def broadcast_stock_update(
        self,
        product_id: str,
        product_name: str,
        branch_id: str,
        branch_name: str,
        quantity: int,
    ):
        """
        Manda a todos los conectados en /ws/stock
        que el stock de un producto cambió.
        """
        message = json.dumps({
            "type": "stock_updated",
            "product_id": product_id,
            "product_name": product_name,
            "branch_id": branch_id,
            "branch_name": branch_name,
            "quantity": quantity,
        })
        await self._broadcast(self.stock, message)

    # ──────────────────────────── Chat ────────────────────────────

    async def send_message(
        self,
        sender_id: str,
        sender_username: str,
        receiver_id: str,
        content: str,
        created_at: str,
    ):
        """
        Manda un mensaje privado al receiver.
        Si el receiver no está conectado el mensaje
        igual queda guardado en la DB.
        """
        message = json.dumps({
            "type": "message",
            "sender_id": sender_id,
            "sender_username": sender_username,
            "content": content,
            "created_at": created_at,
        })

        # mandar al receiver si está conectado
        if receiver_id in self.chat:
            await self.chat[receiver_id].send_text(message)

        # mandar al sender también para confirmar
        if sender_id in self.chat:
            await self.chat[sender_id].send_text(message)

    # ──────────────────────────── Presence ────────────────────────────

    async def broadcast_presence(self, user_id: str, status: str):
        """Notifica a todos los conectados que un usuario cambió su estado."""
        message = json.dumps({
            "type": "presence",
            "user_id": user_id,
            "status": status,
        })
        # broadcast a los tres canales
        await self._broadcast(self.stock, message)
        await self._broadcast(self.chat, message)
        await self._broadcast(self.presence, message)

    def get_online_users(self) -> list[str]:
        """Devuelve los IDs de todos los usuarios conectados."""
        online = set(self.stock.keys()) | set(self.chat.keys()) | set(self.presence.keys())
        return list(online)

    # ──────────────────────────── Utils ────────────────────────────

    async def _broadcast(self, connections: dict[str, WebSocket], message: str):
        """Manda un mensaje a todas las conexiones de un canal."""
        disconnected = []
        for user_id, websocket in connections.items():
            try:
                await websocket.send_text(message)
            except Exception:
                disconnected.append(user_id)

        # limpiar conexiones caídas
        for user_id in disconnected:
            del connections[user_id]


# instancia global — un solo manager para toda la app
manager = ConnectionManager()