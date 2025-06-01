# Muhammad Fajri Firdaus (123140050 )
# Bayu Brigas Novaldi (123140072)
# Kelompok : BOTTOT

from __future__ import annotations

import random
from typing import List, Optional, Tuple

from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from ..util import get_direction


class BottotLogic(BaseLogic):
    # Bot greedy yang sudah ditingkatkan dengan fitur:
    # - mengenali teleporter,
    # - gerakan zig-zag,
    # - menghindari diamond merah saat inventory tinggi (>= 4),
    # - pulang ke base jika sudah cukup diamond (>= 5),
    # - dan kesadaran waktu (pulang ke base jika waktu hampir habis).

    def __init__(self) -> None:
        # Urutan arah: Kanan, Bawah, Kiri, Atas
        self.directions: List[Tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.axis_toggle: bool = False  # Untuk zig-zag: False = prioritas X, True = prioritas Y

    #  Fungsi Utilitas 
    @staticmethod
    def _manhattan(a: Position, b: Position) -> int:
        # Menghitung jarak Manhattan (tanpa diagonal)
        # jalan zig-zag tanpa perpindahan diagonal
        return abs(a.x - b.x) + abs(a.y - b.y)

    @staticmethod
    def _is_red_diamond(obj: GameObject) -> bool:
        # Mengecek apakah objek adalah diamond merah (poin = 2 → dikurangi saat disetor)
        return obj.type == "DiamondGameObject" and getattr(obj.properties, "points", 1) == 2

    # fungsi untuk mendeteksi bahaya
    # jika inventory >= 4, hindari diamond merah
    def _is_dangerous(self, board: Board, pos: Position) -> bool:
        # Menentukan apakah posisi tersebut mengandung diamond merah
        for obj in board.game_objects:
            if obj.position == pos and self._is_red_diamond(obj):
                return True
        return False

    @staticmethod
    def _other_teleporter(entry: GameObject, teleporters: List[GameObject]) -> Optional[GameObject]:
        # Mendapatkan teleporter pasangannya (bukan diri sendiri)
        for tp in teleporters:
            if tp.id != entry.id:
                return tp
        return None

    def _best_teleporter_entry(
        self,
        current: Position,
        dest: Position,
        teleporters: List[GameObject],
    ) -> Tuple[Optional[Position], int]:
        
        # Menentukan pintu masuk teleporter terbaik untuk mendekati tujuan,
        # dibandingkan dengan jarak langsung. Jika tidak lebih baik, tidak menggunakan teleporter.
        direct_distance = self._manhattan(current, dest)
        if len(teleporters) < 2:
            return None, direct_distance

        best_entry: Optional[Position] = None
        best_total: int = direct_distance

        for entry in teleporters:
            exit_ = self._other_teleporter(entry, teleporters)
            if not exit_ or entry.position == current:
                continue
            total = self._manhattan(current, entry.position) + self._manhattan(exit_.position, dest)
            if total < best_total:
                best_total = total
                best_entry = entry.position

        return best_entry, best_total

    # Logika Utama Pergerakan 
    def next_move(self, bot: GameObject, board: Board) -> Tuple[int, int]:
        cur = bot.position
        props = bot.properties
        diamond_count: int = props.diamonds or 0
        base: Optional[Position] = props.base

        # Konversi waktu tersisa dari milidetik ke detik
        milliseconds_left: int = props.milliseconds_left or 0
        seconds_left: int = milliseconds_left // 1000

        # Hitung jarak ke base (digunakan untuk pulang atau perbandingan)
        d_base: int = self._manhattan(cur, base) if base else float("inf")

        # Menentukan Tujuan 
        # Ambil diamond terdekat, hindari diamond merah jika inventory >= 4
        diamonds: List[GameObject] = [
            obj
            for obj in board.game_objects
            if obj.type == "DiamondGameObject" and not (diamond_count >= 4 and self._is_red_diamond(obj))
        ]
        diamonds.sort(key=lambda d: self._manhattan(cur, d.position))
        nearest_diamond: Optional[GameObject] = diamonds[0] if diamonds else None
        d_diamond: int = (
            self._manhattan(cur, nearest_diamond.position) if nearest_diamond else float("inf")
        )

        # Aturan utama penentuan tujuan:
        if diamond_count >= 5:
            dest: Optional[Position] = base  # Sudah cukup diamond, pulang
        elif diamond_count == 0:
            dest = nearest_diamond.position if nearest_diamond else base  # Belum punya diamond, cari
        else:
            dest = nearest_diamond.position if nearest_diamond and d_diamond < d_base else base  # Pilih tergantung jarak

        # Aturan waktu kritis 
        # Jika waktu tersisa tidak cukup untuk pulang, langsung pulang
        if base and seconds_left <= d_base + 1:
            dest = base

        # Jika tidak ada tujuan (misalnya tidak ada base), gerak acak aman
        if dest is None:
            return self._random_safe_move(board, cur, diamond_count)

        # Optimasi dengan Teleporter
        teleporters: List[GameObject] = [o for o in board.game_objects if o.type == "TeleportGameObject"]
        tele_entry, _ = self._best_teleporter_entry(cur, dest, teleporters)
        self.goal_position = tele_entry if tele_entry else dest

        # Zig-zag Menuju Tujuan 
        dx_total: int = self.goal_position.x - cur.x
        dy_total: int = self.goal_position.y - cur.y
        step_x: int = 0 if dx_total == 0 else (1 if dx_total > 0 else -1)
        step_y: int = 0 if dy_total == 0 else (1 if dy_total > 0 else -1)

        candidate_moves: List[Tuple[int, int]] = []
        if self.axis_toggle:  # Y dulu baru X
            if step_y:
                candidate_moves.append((0, step_y))
            if step_x:
                candidate_moves.append((step_x, 0))
        else:  # X dulu baru Y
            if step_x:
                candidate_moves.append((step_x, 0))
            if step_y:
                candidate_moves.append((0, step_y))

        # Coba jalankan langkah zig-zag yang valid dan aman
        for dx, dy in candidate_moves:
            new_pos = Position(cur.x + dx, cur.y + dy)
            if board.is_valid_move(cur, dx, dy) and not (
                diamond_count >= 4 and self._is_dangerous(board, new_pos)
            ):
                self.axis_toggle = not self.axis_toggle
                return dx, dy

        # Alternatif fallback: arah langsung ke tujuan 
        dx, dy = get_direction(cur.x, cur.y, self.goal_position.x, self.goal_position.y)
        new_pos = Position(cur.x + dx, cur.y + dy)
        if board.is_valid_move(cur, dx, dy) and not (
            diamond_count >= 4 and self._is_dangerous(board, new_pos)
        ):
            self.axis_toggle = not self.axis_toggle
            return dx, dy

        # Jika sedang di base, setor diamond 
        if dx == 0 and dy == 0 and base and cur == base and diamond_count > 0:
            props.diamonds = 0
            return 0, 0

        # Langkah terakhir: gerakan aman acak
        return self._random_safe_move(board, cur, diamond_count)

    # Gerakan acak aman 
    def _random_safe_move(self, board: Board, pos: Position, diamond_count: int) -> Tuple[int, int]:
        valid: List[Tuple[int, int]] = []
        for dx, dy in self.directions:
            new_pos = Position(pos.x + dx, pos.y + dy)
            if board.is_valid_move(pos, dx, dy):
                if diamond_count >= 4 and self._is_dangerous(board, new_pos):
                    continue  # Hindari diamond merah saat inventory tinggi
                valid.append((dx, dy))
        return random.choice(valid) if valid else (0, 0)
