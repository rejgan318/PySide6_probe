[[Qt6]] [[конспект]]

[pythonguis: Multithreading PyQt6 applications with QThreadPool](https://www.pythonguis.com/tutorials/multithreading-pyqt6-applications-qthreadpool/)

>Дальше [Using QProcess to run external programs](https://www.pythonguis.com/tutorials/pyqt6-qprocess-external-programs/)

>[!note] Qt Concurrent
>Обратите внимание, что [`QThreadPool`](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThreadPool.html#PySide6.QtCore.PySide6.QtCore.QThreadPool "PySide6.QtCore.PySide6.QtCore.QThreadPool")это низкоуровневый класс для управления потоками, см. модуль [Qt Concurrent](https://doc.qt.io/qtforpython-6/overviews/qtconcurrentrun.html) для альтернатив более высокого уровня.

### class WorkerSignals(QObject)

Косметика. Создает сигналы, которые сохраняются в Worker

``` python
finished = Signal()  
error = Signal(tuple)  
result = Signal(object)  
progress = Signal(int)
```

### class Worker(QRunnable)

Наследуется от QRunnable к настройке рабочего потока обработчика, сигналам и завершению. Сохраняет в self `__init__(self, fn, *args, **kwargs)`
- переданную первым параметром функцию
- аргументы
- создает экземпляр `self.signals = WorkerSignals()`
- ❓`self.kwargs['progress_callback'] = self.signals.progress`
- определяет слот. Запускает функцию fn (из инициализации), при этом либо отлавливает ошибки, либо вызывает сигнал с параметром полученного результата; в любом случает в конце вызывает сигнал `finished`
```python
    @Slot()
    def run(self):
        """ Initialise the runner function with passed args, kwargs """
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

```

Worker - это просто обертка к переданной функции и ее запуск через слот с контролем ошибок и отдача результата через `self.signals.result`

### MainWindow

Обычный интерфейс из виджетов. 

Qlabel `lbl_timer_demo` привязываем к таймеру исключительно для демонстрации, что наше главное окно приложения отзывчиво, работает, и ему не мешают другие задачи, запущенные отдельными потоками. Созданному таймеру назначается обработчик `recurring_timer`, который тут же определен отдельным методом. Просто выводит счетчик секунд с момента старта

Одному из элементов (кнопке btn_RunLongTask) назначается обработчик `btn_RunLongTask.pressed.connect(self.prepare_and_start_task)`

Создается пулл потоков. Для справки выводится максимальное количество одновременно запущенных задач (количество ядер процессора * количество потоком, 2. У меня выдало 12)

```python
        self.threadpool = QThreadPool()
        print(f"Multithreading with maximum {self.threadpool.maxThreadCount()} threads")

```

### prepare_and_start_task

- Создается экземпляр `Worker`. Первый параметр - вызываемая функция. Дальше могут идти параметры функции, в примере их нет
- ему приписываются конкретные callback функции для обработки сигналов от конкретной функции, которая будет вызвана в отдельном потоке
- запускается сформированный `worker` через пул процессов

```python
	worker = Worker(self.my_long_task)
	
	worker.signals.result.connect(self.fn_signal_result)
	worker.signals.finished.connect(self.fn_signal_finished)
	worker.signals.progress.connect(self.fn_signal_progress)

	self.threadpool.start(worker)
```

### calback функции `fn_signal_result`, `fn_signal_progress`, `fn_signal_finished`

В примере эти функции просто делают вывод вывод в консоль. В реальном приложении должны менять элемент интерфейса для визуализации полученного результата (или просто его сохранения для дальнейшего использования), факта окончания задачи или хода процесса. Эти функции назначаются `woker`, который будет вызывать их через вызов сигнала после окончания задачи и получения результата. `fn_signal_progress` вызывается прямо из задачи на промежуточных этапах до ее завершения. Может выдавать проценты от общего прогресса или, например, статус шагов выполнения ('read', 'вычисляем коэффициенты аппроксимации' как шизовые статусы при загрузке Sims 3)