## 学 InfluxDB 源码

### 启动 influxd

/cmd/influxd/main.go 是启动函数，先

```go
rootCmd, err := launcher.NewInfluxdCommand(ctx, v)
```

创建了 rootCmd，然后 ```rootCmd.Execute()``` 执行命令，就是启动 influxd.

跟踪创建 rootCmd 的函数到 /cmd/influxd/launcher/cmd.go，发现这里的 cmd 是调用 ```cli.NewCommand(o.Viper, &prog)``` 创建的，到这里已经没有跟踪的必要了，NewCommand 只是在做一堆环境设置或者 flag 解析。真正启动的程序在 prog 里，prog 是这么来的：

```go
prog := cli.Program{
    Name: "influxd",
    Run:  cmdRunE(ctx, o),
}
```

跟踪启动函数 cmdRunE(/cmd/influxd/launcher/cmd.go)，找到启动代码：

```go
l := NewLauncher()
...
if err := l.run(signals.WithStandardSignals(ctx), o); err != nil {
    return err
}
<-l.Done()
```

这里已经很清楚了，是启动了一个 Launcher 实例，跟踪到 Launcher 结构(/cmd/influxd/launcher/launcher.go) 的 run 函数，终于找到了起点。

### HTTP 收发

在 /cmd/influxd/launcher/launcher.go 的 run 函数里有一堆 http 配置，最后 m.runHTTP() 监听 http 消息，runHTTP() 里最终是调用 m.httpServer 的 Serve 或者 ServeTLS(https) 启动。重要的是 handler：

```go
var httpHandler nethttp.Handler = http.NewRootHandler(
    "platform",
    http.WithLog(httpLogger),
    http.WithAPIHandler(platformHandler),
    http.WithPprofEnabled(!opts.ProfilingDisabled),
    http.WithMetrics(m.reg, !opts.MetricsDisabled),
)
```

继续跟踪 platformHandler 去寻找 API 处理逻辑。现在问题就是 platformHandler 里注册了一大堆 handler 不知道哪个在处理数据库 api：

```go
platformHandler := http.NewPlatformHandler(
    m.apibackend,
    http.WithResourceHandler(stacksHTTPServer),
    http.WithResourceHandler(templatesHTTPServer),
    http.WithResourceHandler(onboardHTTPServer),
    http.WithResourceHandler(authHTTPServer),
    http.WithResourceHandler(labelHandler),
    http.WithResourceHandler(sessionHTTPServer.SignInResourceHandler()),
    http.WithResourceHandler(sessionHTTPServer.SignOutResourceHandler()),
    http.WithResourceHandler(userHTTPServer.MeResourceHandler()),
    http.WithResourceHandler(userHTTPServer.UserResourceHandler()),
    http.WithResourceHandler(orgHTTPServer),
    http.WithResourceHandler(bucketHTTPServer),
    http.WithResourceHandler(v1AuthHTTPServer),
    http.WithResourceHandler(dashboardServer),
)
```

猜测是 ts.bucketHTTPServer ，看了一眼在 /tenant 里，不太靠谱，好像是 meta data 处理的。继续猜测可能是 m.apibackend，

```go
m.apibackend = &http.APIBackend{
    NewBucketService:     source.NewBucketService,
    NewQueryService:      source.NewQueryService,
    PointsWriter: &storage.LoggingPointsWriter{
        Underlying:    pointsWriter,
        BucketFinder:  ts.BucketService,
        LogBucketName: platform.MonitoringSystemBucketName,
    },
    BucketService:                   ts.BucketService,
    UserService:                     ts.UserService,
    InfluxQLService:                 storageQueryService,
    InfluxqldService:                iqlquery.NewProxyExecutor(m.log, qe),
    FluxService:                     storageQueryService,
    FluxLanguageService:             fluxlang.DefaultService,
}
```

其实里面还有一大堆 Service，太长都给省略了。跟踪 pointsWriter：

```go
var (
    deleteService  platform.DeleteService  = m.engine
    pointsWriter   storage.PointsWriter    = m.engine
    backupService  platform.BackupService  = m.engine
    restoreService platform.RestoreService = m.engine
)
```

原来都在 storage 里，

```go
m.engine = storage.NewEngine(
    opts.EnginePath,
    opts.StorageConfig,
    storage.WithMetaClient(metaClient),
)
```

在 /storage/engine.go 里找到了 WritePoints，它是接受了 points []models.Point 作为参数，在 /models/points.go 里终于找到了把 Line Protocol 解析到 Point Struct 的代码。在 httpHandler 里应该会调用这个构造 points 然后送到 writePoints 里。

