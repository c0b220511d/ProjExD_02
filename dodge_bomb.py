import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  #練習3:押下キーと移動量の辞書
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
}

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを返す関数
    引数 rct:こうかとんor爆弾SurfaceのRect
    戻り値:横方向、縦方向はみ出し判定結果(画面内:True/画面外:False)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return (yoko, tate)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_sad_img = pg.image.load("ex02/fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_sad_img = pg.transform.rotozoom(kk_sad_img, 0, 2.0)
    kk_hanten_img = pg.transform.flip(kk_img, True, False)
    kaiten = {
        (-5, -5):pg.transform.rotozoom(kk_img, -45, 1.0),
        (-5, 0):kk_img,
        (-5, +5):pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, +5):pg.transform.rotozoom(kk_img, 90, 1.0),
        (+5, +5):pg.transform.rotozoom(kk_hanten_img, -45, 1.0),
        (+5, 0):kk_hanten_img,
        (+5, -5):pg.transform.rotozoom(kk_hanten_img, 45, 1.0),
        (0, -5):pg.transform.rotozoom(kk_hanten_img, 90, 1.0)
    }
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))  # 練習1:透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 練習1:黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習1:赤い半径10の円を描く
    bb_rct = bb_img.get_rect()  # 練習2: 爆弾SurfaceのRectを抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習2:爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    flag = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        
        mv_tpl = tuple(sum_mv)
        for k, val in kaiten.items():  # 追加機能1
            if mv_tpl == k:
                kk_img = val

        if kk_rct.colliderect(bb_rct):  # 追加機能3
            flag = 1
            kk_img = kk_sad_img
        
        screen.blit(kk_img, kk_rct)  # 練習3:こうかとんを移動させる

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        bb_rct.move_ip(vx, vy)  # 練習2:爆弾を移動させる
        for i in range(int(tmr/50)):  # 追加化機能2
            bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if flag:  # 追加機能3
            clock.tick(1)
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()