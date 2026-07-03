import pyxel
import random

class Player:
    def __init__(self):
        self.w = 5
        self.h = 5
        self.x = 100 - self.w // 2
        self.y = 100 - self.h // 2
        self.base_speed = 2
        self.speed = 2
        
        self.speed_timer = 0
        self.speed_state = "normal"

    def update(self):
        if self.speed_timer > 0:
            self.speed_timer -= 1
            if self.speed_timer == 0:
                self.speed_state = "normal"
                self.speed = self.base_speed
        
        if self.speed_state == "fast":
            self.speed = self.base_speed * 2
        elif self.speed_state == "slow":
            self.speed = max(1, self.base_speed // 2)
        else:
            self.speed = self.base_speed

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed

        self.x = max(0, min(200 - self.w, self.x))
        self.y = max(0, min(200 - self.h, self.y))

    def draw(self):
        color = 0
        if self.speed_state == "fast":
            color = 11
        elif self.speed_state == "slow":
            color = 4
        pyxel.rect(self.x, self.y, self.w, self.h, color)


class Bomb:
    def __init__(self, player_x, player_y, existing_bombs, min_rate, max_rate, start_pos=None):
        self.type = random.choice(['circle', 'square'])
        self.timer = 0
        self.size = 5.0
        self.is_active = False
        self.expansion_rate = random.uniform(min_rate, max_rate)

        if start_pos is not None:
            self.x, self.y = start_pos
        else:
            while True:
                self.x = random.randint(0, 200)
                self.y = random.randint(0, 200)
                
                px_center = player_x + 2.5
                py_center = player_y + 2.5
                if (self.x - px_center)**2 + (self.y - py_center)**2 <= 20**2:
                    continue
                    
                overlapped = False
                for ob in existing_bombs:
                    if hasattr(ob, 'x') and (self.x - ob.x)**2 + (self.y - ob.y)**2 <= 15**2:
                        overlapped = True
                        break
                if not overlapped:
                    break

    def update(self):
        self.timer += 1
        if self.timer == 30:
            self.is_active = True
        
        if self.is_active and self.timer % 3 == 0:
            self.size += self.expansion_rate

    def draw(self):
        color = 8 if self.is_active else 12
        draw_size = int(self.size)

        if self.type == 'circle':
            pyxel.circ(self.x, self.y, draw_size, color)
        elif self.type == 'square':
            half = draw_size / 2
            pyxel.rect(self.x - half, self.y - half, draw_size, draw_size, color)

    def check_hit(self, px, py, pw, ph):
        if not self.is_active:
            return False
        cx = px + pw / 2
        cy = py + ph / 2

        if self.type == 'circle':
            return (cx - self.x)**2 + (cy - self.y)**2 <= self.size**2
        elif self.type == 'square':
            half = self.size / 2
            return (self.x - half <= cx <= self.x + half) and (self.y - half <= cy <= self.y + half)


class SpeedItem:
    def __init__(self, item_type, player_x, player_y, existing_bombs):
        self.item_type = item_type
        self.timer = 0
        self.size = 5.0
        self.is_active = False
        self.expansion_rate = 1.5

        while True:
            self.x = random.randint(20, 180)
            self.y = random.randint(20, 180)
            px_center = player_x + 2.5
            py_center = player_y + 2.5
            if (self.x - px_center)**2 + (self.y - py_center)**2 <= 20**2:
                continue
            overlapped = False
            for ob in existing_bombs:
                if hasattr(ob, 'x') and (self.x - ob.x)**2 + (self.y - ob.y)**2 <= 15**2:
                    overlapped = True
                    break
            if not overlapped:
                break

    def update(self):
        self.timer += 1
        if self.timer == 30:
            self.is_active = True
        if self.is_active and self.timer % 3 == 0:
            self.size += self.expansion_rate

    def draw(self):
        if self.is_active:
            color = 11 if self.item_type == "fast" else 4
        else:
            color = 12
            
        half = int(self.size) / 2
        pyxel.rect(self.x - half, self.y - half, int(self.size), int(self.size), color)

    def check_hit(self, px, py, pw, ph):
        if not self.is_active:
            return False
        cx = px + pw / 2
        cy = py + ph / 2
        half = self.size / 2
        return (self.x - half <= cx <= self.x + half) and (self.y - half <= cy <= self.y + half)


class CrossBomb:
    def __init__(self, player_x, player_y, existing_bombs):
        self.timer = 0
        self.width = 10.0      
        self.wing_length = 0.0 
        self.is_active = False

        while True:
            self.x = random.randint(0, 200)
            self.y = random.randint(0, 200)
            
            px_center = player_x + 2.5
            py_center = player_y + 2.5
            if (self.x - px_center)**2 + (self.y - py_center)**2 <= 25**2:
                continue
                
            overlapped = False
            for ob in existing_bombs:
                if hasattr(ob, 'x') and (self.x - ob.x)**2 + (self.y - ob.y)**2 <= 20**2:
                    overlapped = True
                    break
            if not overlapped:
                break

    def update(self):
        self.timer += 1
        if self.timer == 30:
            self.is_active = True
            
        if self.is_active and self.timer % 3 == 0:
            self.wing_length += 4.0
            self.width += 0.1

    def draw(self):
        color = 9 if self.is_active else 10 
        w = int(self.width)
        half_w = w / 2
        pyxel.rect(self.x - half_w, self.y - half_w, w, w, color)
        
        if self.wing_length > 0:
            wl = int(self.wing_length)
            pyxel.rect(self.x - half_w - wl, self.y - half_w, wl, w, color)
            pyxel.rect(self.x + half_w, self.y - half_w, wl, w, color)
            pyxel.rect(self.x - half_w, self.y - half_w - wl, w, wl, color)
            pyxel.rect(self.x - half_w, self.y + half_w, w, wl, color)

    def check_hit(self, px, py, pw, ph):
        if not self.is_active:
            return False
        
        half_w = self.width / 2
        wl = int(self.wing_length)
        
        cross_left = self.x - half_w - wl
        cross_right = self.x + half_w + wl
        horiz_hit = (px < cross_right and px + pw > cross_left and 
                     py < self.y + half_w and py + ph > self.y - half_w)
        
        cross_top = self.y - half_w - wl
        cross_bottom = self.y + half_w + wl
        vert_hit = (px < self.x + half_w and px + pw > self.x - half_w and 
                    py < cross_bottom and py + ph > cross_top)
        
        return horiz_hit or vert_hit


class App:
    def __init__(self):
        pyxel.init(200, 200, title="情報ボンバーマン")
        self.scene = "SELECT" 
        self.mode = "easy"
        self.help_page = 1 # 💡 説明画面用のページ番号管理（1〜2）
        pyxel.run(self.update, self.draw)

    def init_game(self):
        self.player = Player()
        self.bombs = []
        self.cross_bombs = []
        self.speed_items = []   
        self.score = 0
        self.life = 10
        
        self.spawn_timer = 0
        self.item_spawn_timer = 0
        self.cross_spawn_timer = 0
        self.corner_spawn_timer = 0 
        self.fast_spawn_timer = 0   
        self.slow_spawn_timer = 0   
        
        self.item_active = False
        self.item_x = 0
        self.item_y = 0
        self.item_timer = 0

    def update(self):
        if self.scene == "SELECT":
            if pyxel.btnp(pyxel.KEY_1):
                self.mode = "easy"; self.scene = "READY"; self.init_game()
            elif pyxel.btnp(pyxel.KEY_2):
                self.mode = "normal"; self.scene = "READY"; self.init_game()
            elif pyxel.btnp(pyxel.KEY_3):
                self.mode = "hard"; self.scene = "READY"; self.init_game()
            elif pyxel.btnp(pyxel.KEY_4):
                # 💡 4のキーで説明画面へ移動
                self.scene = "HELP"
                self.help_page = 1
            return

        elif self.scene == "HELP":
            # 💡 左右の矢印キーでページ移動、Enterキーで戻る
            if pyxel.btnp(pyxel.KEY_LEFT):
                self.help_page = max(1, self.help_page - 1)
            elif pyxel.btnp(pyxel.KEY_RIGHT):
                self.help_page = min(2, self.help_page + 1)
            elif pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = "SELECT"
            return

        elif self.scene == "READY":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = "PLAY"
                pyxel.play(0, 3, loop=True)
            return

        elif self.scene == "GAMEOVER":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = "SELECT"
            return

        if self.life <= 0:
            self.scene = "GAMEOVER"
            pyxel.stop(0)
            pyxel.play(0, 0)
            return

        self.player.update()

        self.spawn_timer += 1
        self.item_spawn_timer += 1
        self.corner_spawn_timer += 1   
        self.fast_spawn_timer += 1     
        self.slow_spawn_timer += 1     
        if self.mode == "hard":
            self.cross_spawn_timer += 1

        min_rate, max_rate = (1.0, 2.0) if self.mode == "easy" else (2.0, 3.0)

        # 通常爆弾（5秒ごと）
        if self.spawn_timer >= 150:
            self.spawn_timer = 0
            num_bombs = random.randint(7, 10)
            for _ in range(num_bombs):
                all_existing = self.bombs + self.cross_bombs + self.speed_items
                self.bombs.append(Bomb(self.player.x, self.player.y, all_existing, min_rate, max_rate))

        # 十字爆弾（10秒ごと、Hardのみ）
        if self.mode == "hard" and self.cross_spawn_timer >= 300:
            self.cross_spawn_timer = 0
            all_existing = self.bombs + self.cross_bombs + self.speed_items
            self.cross_bombs.append(CrossBomb(self.player.x, self.player.y, all_existing))

        # 4隅爆弾の生成（10秒に1回、ランダムな2隅から出現、性能は通常爆弾と統一）
        if self.corner_spawn_timer >= 300:
            self.corner_spawn_timer = 0
            corners = [(0, 0), (200, 0), (0, 200), (200, 200)]
            chosen_corners = random.sample(corners, 2)
            for pos in chosen_corners:
                all_existing = self.bombs + self.cross_bombs + self.speed_items
                self.bombs.append(Bomb(self.player.x, self.player.y, all_existing, min_rate, max_rate, start_pos=pos))

        # 加速アイテムの生成（15秒に1回）
        if self.fast_spawn_timer >= 450:
            self.fast_spawn_timer = 0
            all_existing = self.bombs + self.cross_bombs + self.speed_items
            self.speed_items.append(SpeedItem("fast", self.player.x, self.player.y, all_existing))

        # 減速アイテムの生成（15秒に1回）
        if self.slow_spawn_timer >= 450:
            self.slow_spawn_timer = 0
            all_existing = self.bombs + self.cross_bombs + self.speed_items
            self.speed_items.append(SpeedItem("slow", self.player.x, self.player.y, all_existing))

        # --- 各種オブジェクトの衝突・更新ループ ---

        # 爆弾
        for b in self.bombs[:]:
            b.update()
            if b.check_hit(self.player.x, self.player.y, self.player.w, self.player.h):
                self.life -= 1
                pyxel.play(1, 1)
                self.bombs.remove(b)
                continue
            if b.timer >= 120:
                self.score += 1
                self.bombs.remove(b)

        # 十字爆弾
        for cb in self.cross_bombs[:]:
            cb.update()
            if cb.check_hit(self.player.x, self.player.y, self.player.w, self.player.h):
                self.life -= 2
                pyxel.play(1, 1)
                self.cross_bombs.remove(cb)
                continue
            if cb.timer >= 180:
                self.score += 1
                self.cross_bombs.remove(cb)

        # 速度変更アイテム
        for si in self.speed_items[:]:
            si.update()
            if si.check_hit(self.player.x, self.player.y, self.player.w, self.player.h):
                self.player.speed_timer = 450
                self.player.speed_state = si.item_type
                pyxel.play(1, 2)
                self.speed_items.remove(si)
                continue
            if si.timer >= 120:
                self.score += 1
                self.speed_items.remove(si)

        # 回復アイテム（30秒ごと、サイズを倍に変更）
        if self.item_spawn_timer >= 900:
            self.item_spawn_timer = 0
            self.item_active = True
            self.item_x = random.randint(20, 160)
            self.item_y = random.randint(20, 160)
            self.item_timer = 0
        
        if self.item_active:
            self.item_timer += 1
            if self.item_timer >= 240:
                self.item_active = False
            
            is_on_item = (self.player.x < self.item_x + 20 and 
                          self.player.x + self.player.w > self.item_x and
                          self.player.y < self.item_y + 20 and 
                          self.player.y + self.player.h > self.item_y)
            
            if is_on_item and pyxel.btnp(pyxel.KEY_RETURN):
                self.life += 1
                pyxel.play(1, 2)
                self.item_active = False

    def draw(self):
        pyxel.cls(7)
        
        if self.scene == "SELECT":
            pyxel.text(50, 40, "SELECT STAGE", 0)
            pyxel.text(55, 70, "1 : EASY", 1)
            pyxel.text(55, 90, "2 : NORMAL", 2)
            pyxel.text(55, 110, "3 : HARD", 8)
            pyxel.text(55, 140, "4 : HOW TO PLAY", 4) # 💡 ガイドを追加
            return

        elif self.scene == "HELP":
            # 💡 説明画面の描画処理
            pyxel.text(10, 10, f"--- HOW TO PLAY ({self.help_page}/2) ---", 0)
            
            if self.help_page == 1:
                pyxel.text(10, 35, "[BASIC RULE]", 8)
                pyxel.text(15, 47, "- MOVE : ARROW KEYS", 0)
                pyxel.text(15, 59, "- AVOID EXPANDING BOMBS!", 0)
                pyxel.text(15, 71, "- TIME LIMIT TO SURVIVE", 0)
                
                pyxel.text(10, 95, "[PLAYER STATUS & COLOR]", 8)
                pyxel.rect(15, 110, 5, 5, 0)
                pyxel.text(25, 110, "BLACK  : NORMAL SPEED", 0)
                
                pyxel.rect(15, 125, 5, 5, 11)
                pyxel.text(25, 125, "GREEN  : FAST (2x SPEED)", 11)
                
                pyxel.rect(15, 140, 5, 5, 4)
                pyxel.text(25, 140, "NAVY   : SLOW (0.5x SPEED)", 4)
                
            elif self.help_page == 2:
                pyxel.text(10, 30, "[OBJECT DIRECTORY]", 8)
                
                # 通常爆弾
                pyxel.circ(17, 47, 3, 8)
                pyxel.text(27, 45, "GRAY->RED : NORMAL BOMB (-1 LIFE)", 0)
                
                # 十字爆弾
                pyxel.rect(14, 62, 6, 6, 9)
                pyxel.text(27, 62, "ORANGE    : CROSS BOMB  (-2 LIFE)", 9)
                
                # 加速アイテム
                pyxel.rect(14, 80, 6, 6, 11)
                pyxel.text(27, 80, "GREEN SQ  : SPEED UP ITEM", 11)
                
                # 減速アイテム
                pyxel.rect(14, 98, 6, 6, 4)
                pyxel.text(27, 98, "NAVY SQ   : SPEED DOWN ITEM", 4)
                
                # 回復アイテム
                pyxel.rect(12, 113, 10, 10, 14)
                pyxel.text(27, 116, "PINK SQ   : RECOVERY (+1 LIFE)", 14)
                pyxel.text(27, 126, "            *PRESS ENTER ON IT", 0)

            # 下部ナビゲーション
            pyxel.text(15, 170, "LEFT/RIGHT : CHANGE PAGE", 1)
            pyxel.text(15, 182, "PRESS ENTER : RETURN TO MENU", 2)
            return

        elif self.scene == "READY":
            pyxel.text(55, 80, f"MODE: {self.mode.upper()}", 0)
            pyxel.text(65, 110, "Enter start", 8)
            return

        elif self.scene == "GAMEOVER":
            pyxel.text(80, 75, "GAME OVER", 8)
            pyxel.text(66, 96, "YOUR SCORE", 0)
            pyxel.text(91, 110, f"[ {self.score} ]", 0)
            pyxel.text(42, 140, "PRESS ENTER TO SELECT", 1)
            return

        for b in self.bombs: b.draw()
        for cb in self.cross_bombs: cb.draw()
        for si in self.speed_items: si.draw()     
        
        if self.item_active:
            pyxel.rect(self.item_x, self.item_y, 20, 20, 14)

        self.player.draw()

        pyxel.text(5, 5, "SCORE:" + str(self.score), 0)
        pyxel.text(160, 5, "LIFE:" + str(self.life), 0)
        
        if self.player.speed_timer > 0:
            sec = self.player.speed_timer // 30 + 1
            status_text = f"FAST!! ({sec}s)" if self.player.speed_state == "fast" else f"SLOW.. ({sec}s)"
            text_color = 11 if self.player.speed_state == "fast" else 4
            pyxel.text(80, 5, status_text, text_color)


App()
