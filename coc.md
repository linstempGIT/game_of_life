### 传入参数规范
按参数创建的顺序先后传入
settings -> screen -> cells_group
函数内部的嵌套函数的参数传入顺序为：
外部函数的参数顺序+内部闭包变量的创建顺序
外部(screen -> cells_group) -> 闭包event

### game_function和display_funcion
game_function主要用于处理游戏运行逻辑，
输入事件处理等
display_function主要用于更新元素，渲染元素，
输出屏幕等

## 其他注意事项
连续的函数语句块之间用两行空行隔开，以增强其可读性