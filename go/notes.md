## 类型系统
:= 和 var 定义出来有什么区别？好像 a:=1 和 var a=1 是一样的

默认整数是 int(几位看系统)，小数是 float64(这个看不看系统？不看)，虚数是 complex128(?)
超过 int 的整数类型是什么？

byte=uint8, rune=int32
字符是 int32（语义上是 rune literal），可以 a:='你', b='好'
等价于 a:=20320, b:=22909，在 fmt.Printf 里用 %c 输出变成中文字符

uintptr 是什么？

Type(v), 有没有隐式转换/必须显式转换？比如 math.Sqrt() 必须 float64 一下才能传入，连 float32 都不行。同理定义赋值也一样没有显式转换？

const a=1<<500 这个值是准确的，神秘，这是什么类型？
const 没有指定类型，到底是直接字面量替代的（宏），还是实际有内存的?
我猜是有实际内存的，从报错可以看到类型是 untyped int constant，很长一串，是精确的。

是不是 constant 和字面量都是 untyped？然后只有 untyped 可以隐式转换到 typed？我觉得这个猜想是合理的，毕竟这个只有单向的，typed 没法转换到 untyped，互相之间只能显式

发现字面量也被视作 untyped int constant 和常量是同一个东西

## Control Flow
```go
if v := math.Pow(x, n); v < lim {
    return v
}
```

```go
switch os := runtime.GOOS; os {
case "darwin":
    fmt.Println("OS X.")
case "linux":
    fmt.Println("Linux.")
default:
    // freebsd, openbsd,
    // plan9, windows...
    fmt.Printf("%s.\n", os)
}
```
case 后面可以不是常量，不用每句加 break，只会执行第一块匹配

```go
switch {
case t.Hour() < 12:
    fmt.Println("Good morning!")
case t.Hour() < 17:
    fmt.Println("Good afternoon.")
default:
    fmt.Println("Good evening.")
}
```

defer 延迟到当前环境 return 后执行，多句是个栈。一般配合中间的 return 做点 close 工作。函数里的值是读到 defer 语句的时候确定的，后续改变不影响。能用在非函数上吗？

## 指针和结构
p=&i
结构体指针的 dereference 可以直接写成 `p.X`，等价于`(*p).X`

C 的指针=起始地址+元素类型(或者说是它的补长/宽度/size)
```go
var (
    v1 = Vertex{1, 2}  // has type Vertex
    v2 = Vertex{X: 1}  // Y:0 is implicit
    v3 = Vertex{}      // X:0 and Y:0
    p  = &Vertex{1, 2} // has type *Vertex
    q = &Vertex{1, 2} // q != p
)
```

常量不能取指针，结构体不能作为常量。

## 数组与切片
```go
primes := [6]int{2, 3, 5, 7, 11, 13}
// primes := [...]int{2, 3, 5, 7, 11, 13}
var s []int = primes[1:4]
```
切片不是拷贝，是 reference, array length 不能是变量

```go
s := []struct {
    i int
    b bool
}{
    {2, true},
    {3, false},
    {5, true},
    {7, true},
    {11, false},
    {13, true},
}
```
切片可以 resize 到 len 之外，但不能超过 cap，切头会丢失，resize 不能填负数
```go
len(s)
cap(s)
make([]int, 5) // len=cap=5
make([]int, 1, 5) // len=1,cap=5
```
为什么设计 slice？有什么好处？
make 是什么关键字？

```go
a := []int{1, 2, 3, 4}
var b []int = a[0:3]
b = append(b, 5) // a={1,2,3,5},发生覆盖
b = append(b, 6) // a={1,2,3,5},cap(b)=8
b[0] = 7 // a 不变，b 已经指向新的内存了
```
按我的理解，array 唯一的存在意义就是数组常量，否则就不用 array，全用 slice

这个 slice 未扩大 cap 之前共享一块内存，扩大之后不是同一块，这设计合理吗？就好比在 c++ 里，对 vector 元素取 &。

slice 的 internal 就是起始指针、len、cap 而已。（指针包括元素类型，用来计算宽度的）

怎么取等？怎么判断起始指针相等？怎么判断值相等？

`copy(dst, src []T) int` 宣称可以处理同源数组拷贝，怎么做到的？最低效就是弄一个中间 slice，如果是判断重合区间就可以 $O(1)$ 额外空间。长短不同拷贝数量更小的那个。

自己测试 append 一个值只会翻倍 cap。[官方介绍](https://go.dev/blog/slices-intro) 偷懒说是 (new_cap+1)*2，其实是 cap $0$ 变 $1$ 非 $0$ 翻倍。append 多个值超过两倍 cap 会变成 ceil\[new_cap/2\]*2，合理。

```go
a = append(a, b...) // equivalent to "append(a, b[0], b[1], b[2])"
```

什么时候 copy 什么时候 reference？如果源切片别的都不需要，可以使用 copy 自动把源回收。

### 遍历
```go
for i, v := range pow {}
```
可以省略 v, 只会到 len 不会到 cap

## 映射
```go
type Vertex struct {
	Lat, Long float64
}

var m = map[string]Vertex{
	"Bell Labs": {40.68433, -74.39967},
	"Google":    {37.42202, -122.08408},
}
```

```go
delete(m, "Answer")
v, ok := m["Answer"] // ok(bool) 表示有无该键
```
用上面这个 test 会在 map 中实际生成 entry 吗？这会导致空间浪费吧？还是说没有实际生成，返回值是默认值？
insert 和 update 都是 `m[k]=v`.

## 闭包
```go
func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

func main() {
	pos, neg := adder(), adder()
	for i := 0; i < 10; i++ {
		fmt.Println(
			pos(i),
			neg(-2*i),
		)
	}
}
```
为什么这两个 sum 不同？那如何构建闭包之间的沟通手段？

## 类方法
receiver
```go
func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}
```
上面那个只读，下面那个修改了类成员。

receiver 只能给同包的结构声明，int float 在别的包被定义，所以无法声明 receiver。
（不过可以给一个等价的类型如 `type MyFloat float64`）
## nil
以后弄弄懂。
## 高效写法
https://go.dev/doc/effective_go

