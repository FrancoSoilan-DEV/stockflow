# routers/ws.py
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_access_token
from core.ws_manager import manager
from db.session import get_db, AsyncSessionLocal
from models.models import Message
from services.auth import get_user_by_id
import uuid

router = APIRouter(tags=["websockets"])


async def get_user_from_token(token: str):
    """
    Valida el token JWT en la conexión WebSocket.
    Los WebSockets no usan headers HTTP normales
    por eso el token viaja como query param.
    """
    if not token:
        return None

    payload = decode_access_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    async with AsyncSessionLocal() as db:
        user = await get_user_by_id(db, uuid.UUID(user_id))
        return user


# ──────────────────────────── Stock ────────────────────────────

@router.websocket("/ws/stock")
async def websocket_stock(
    websocket: WebSocket,
    token: str = "",
):
    """
    Canal de stock en tiempo real.
    Recibe notificaciones cuando el stock cambia en cualquier sucursal.
    Uso: ws://localhost:8000/ws/stock?token=eyJhbGc...
    """
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = str(user.id)
    await manager.connect("stock", user_id, websocket)

    # mandar lista de usuarios online al conectar
    await websocket.send_text(
        __import__("json").dumps({
            "type": "online_users",
            "users": manager.get_online_users(),
        })
    )

    try:
        while True:
            # mantener la conexión abierta — el stock se actualiza desde HTTP
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect("stock", user_id)


# ──────────────────────────── Chat ────────────────────────────

@router.websocket("/ws/chat")
async def websocket_chat(
    websocket: WebSocket,
    token: str = "",
):
    """
    Canal de chat entre usuarios.
    Uso: ws://localhost:8000/ws/chat?token=eyJhbGc...

    Para mandar un mensaje enviá:
    {
        "receiver_id": "uuid-del-receptor",
        "content": "Hola, ¿tienen teclados?"
    }
    """
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = str(user.id)
    await manager.connect("chat", user_id, websocket)

    # mandar lista de usuarios online al conectar
    await websocket.send_text(
        __import__("json").dumps({
            "type": "online_users",
            "users": manager.get_online_users(),
        })
    )

    try:
        while True:
            # esperar mensajes del cliente
            data = await websocket.receive_json()

            receiver_id = data.get("receiver_id")
            content = data.get("content")

            if not receiver_id or not content:
                await websocket.send_text(
                    __import__("json").dumps({
                        "type": "error",
                        "detail": "receiver_id y content son requeridos",
                    })
                )
                continue

            # guardar el mensaje en la DB
            async with AsyncSessionLocal() as db:
                message = Message(
                    sender_id=user.id,
                    receiver_id=uuid.UUID(receiver_id),
                    content=content,
                )
                db.add(message)
                await db.commit()
                await db.refresh(message)

            # mandar el mensaje al receiver y confirmar al sender
            await manager.send_message(
                sender_id=user_id,
                sender_username=user.username,
                receiver_id=receiver_id,
                content=content,
                created_at=datetime.now(timezone.utc).isoformat(),
            )

    except WebSocketDisconnect:
        await manager.disconnect("chat", user_id)


# ──────────────────────────── Presence ────────────────────────────

@router.websocket("/ws/presence")
async def websocket_presence(
    websocket: WebSocket,
    token: str = "",
):
    """
    Canal de presencia — quién está online.
    Uso: ws://localhost:8000/ws/presence?token=eyJhbGc...
    """
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = str(user.id)
    await manager.connect("presence", user_id, websocket)

    # mandar lista de usuarios online al conectar
    await websocket.send_text(
        __import__("json").dumps({
            "type": "online_users",
            "users": manager.get_online_users(),
        })
    )

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect("presence", user_id)