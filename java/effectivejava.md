### 提供静态工厂方法
比如 static newSomething(), Boolean.valueOf(),Instant.from(),Map.of(). 用静态方法去构造实例。优点：有名字，不容易弄错；不会每次调用都创建；返回的东西很灵活，可以子类，可以不同，外部可以不知道返回的类，重用不可变对象。缺点：有，但是看不懂。
### 参数太多用 builder
builder 的好处很多。兼具 build 之前可变的灵活性和 build 之后不可变的安全性。
### 怎么写单例
### 依赖注入
### 垃圾回收
比如出栈，```stack[size] = null; size--;```，其实也没什么用。
### try with resources
### 访问权限
提到了一个例子：公共常量数组（也可以改成 List 返回）
```java
private static final Thing[] PRIVATE_VALUES = { ... };
public static final Thing[] values() {
    return PRIVATE_VALUES.clone();
}
```
总之直接 public static final Something[] 是无法起到 final 的作用的。
### 最小化可变性
不可变对象的有点非常多。尽量用。
String 不可变，所以它的拷贝构造其实是不该用的。
### 组合优于继承