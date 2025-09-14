#!/system/bin/sh
# 无限循环，每10秒上滑一次
while true
do
    # 获取屏幕分辨率
    size=$(wm size | awk '{print $3}')
    width=$(echo $size | cut -d'x' -f1)
    height=$(echo $size | cut -d'x' -f2)

    # 计算滑动坐标（从底部中间 -> 顶部中间）
    start_x=$((width / 2))
    start_y=$((height * 4 / 5))
    end_x=$((width / 2))
    end_y=$((height / 5))

    # 执行滑动
    input swipe $start_x $start_y $end_x $end_y 500

    # 间隔10秒
    sleep 10
done
