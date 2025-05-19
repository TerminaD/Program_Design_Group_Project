# 项目架构

该项目文件树示范如下：

```
Program_Design_Group_Project/
├── app.py		# 代码运行入口
├── gui/		# GUI
│   └── main_window.py
│   └── secondary_window.py
│   └── ...
├── backend/	# 后端，连接其他各组件之间的相互调用
│   └── controller.py
│   └── ...
├── crawler/	# 爬虫
│   └── portal_scraper.py
│   └── portal_openjudge.py
│   └── portal_canvas.py
│   └── ...
└── data/		# 数据库逻辑（也由叶高翔负责）
    └── database.py
	└── ...
```

用几个例子说明各文件间的调用关系：
1. **初始化**：`app.py` 调用 GUI 代码、后端代码、数据库代码中的初始化函数，初始化各组件
2. **GUI 中用户显示/更改/删除数据**：GUI 代码调用后端中暴露的函数，后端逻辑再调用数据库代码暴露的函数，从本地存储中显示/更改/删除数据
3. **爬虫**：当条件满足（如用户按下按钮、有一天没更新了），后端调用爬虫代码中暴露的函数，使爬虫在各网站爬取数据，然后爬虫调用后端暴露的函数来储存/更新数据，后端再调用数据库代码中的函数在 SQL 数据库中储存/更新数据

# 如何协作

1. 每个人负责自己的组件（阿扎特负责 `gui`, 罗淞负责 `crawler`, 叶高翔负责`backend`和`data`）。
2. 如果需要某个组件暴露某个借口，和负责同学沟通。
3. 版本管理：每个人从 `main` 分支出一个新 branch，实现好自己部分的功能并 debug 完成后 merge 回 `main`。

# 依赖管理

1. 使用 `conda` 进行依赖包管理。具体可搜索 `conda` 用法。
2. 可从 `environment.yml` 直接创建环境。
3. 如果你新写的代码需要下载新的包，使用 `conda env export > environment.yml` 更新 `environment.yml`，然后 push 到 GitHub。

# 代码格式

1. 类的命名格式为 `ThisIsAClass`，变量的命名格式为 `this_is_a_variable`。
2. 请安装 Black Formatter，随时格式化代码。
3. 请使用英文命名变量，不要使用汉语拼音。
4. 对于逻辑和作用不显然的代码，写备注。
