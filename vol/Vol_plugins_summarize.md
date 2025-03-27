# Vol的插件及功能汇总大全

## Vol3

### Linux 插件

1. **`linux.bash.Bash`**
   - **功能**：从内存中恢复 Bash shell 的命令历史记录。
   - **用法**：`python3 vol.py -f <memory.dump> linux.bash`
   - **说明**：提取进程内存中与 Bash 相关的历史命令，适用于调查用户操作记录。

2. **`linux.boottime.Boottime`**
   - **功能**：显示系统启动时间。
   - **用法**：`python3 vol.py -f <memory.dump> linux.boottime`
   - **说明**：从内核数据结构中提取系统启动时间戳，便于时间线分析。

3. **`linux.capabilities.Capabilities`**
   - **功能**：列出进程的 Linux 权限（capabilities）。
   - **用法**：`python3 vol.py -f <memory.dump> linux.capabilities`
   - **说明**：检查每个进程的权限集，可能用于检测提权行为。

4. **`linux.check_afinfo.Check_afinfo`**
   - **功能**：验证网络协议操作函数指针是否被篡改。
   - **用法**：`python3 vol.py -f <memory.dump> linux.check_afinfo`
   - **说明**：检测潜在的 rootkit 或网络钩子，用于安全分析。

5. **`linux.check_creds.Check_creds`**
   - **功能**：检查是否有进程共享凭据结构。
   - **用法**：`python3 vol.py -f <memory.dump> linux.check_creds`
   - **说明**：异常的凭据共享可能表明权限提升或恶意行为。

6. **`linux.check_idt.Check_idt`**
   - **功能**：检查中断描述符表（IDT）是否被修改。
   - **用法**：`python3 vol.py -f <memory.dump> linux.check_idt`
   - **说明**：用于检测低级内核钩子或 rootkit。

7. **`linux.check_modules.Check_modules`**
   - **功能**：将模块列表与 sysfs 信息对比，验证完整性。
   - **用法**：`python3 vol.py -f <memory.dump> linux.check_modules`
   - **说明**：帮助发现隐藏或篡改的内核模块。

8. **`linux.check_syscall.Check_syscall`**
   - **功能**：检查系统调用表是否被钩子修改。
   - **用法**：`python3 vol.py -f <memory.dump> linux.check_syscall`
   - **说明**：检测常见的 rootkit 技术。

9. **`linux.ebpf.EBPF`**
   - **功能**：枚举 eBPF（扩展伯克利包过滤器）程序。
   - **用法**：`python3 vol.py -f <memory.dump> linux.ebpf`
   - **说明**：检查内核中运行的 eBPF 程序，可能用于网络监控或恶意行为。

10. **`linux.elfs.Elfs`**
    - **功能**：列出所有进程映射的 ELF 文件。
    - **用法**：`python3 vol.py -f <memory.dump> linux.elfs`
    - **说明**：分析进程加载的可执行文件和库。

11. **`linux.envars.Envars`**
    - **功能**：列出进程及其环境变量。
    - **用法**：`python3 vol.py -f <memory.dump> linux.envars`
    - **说明**：提取环境变量以了解进程上下文或配置。

12. **`linux.graphics.fbdev.Fbdev`**
    - **功能**：从 fbdev 图形子系统中提取帧缓冲区。
    - **用法**：`python3 vol.py -f <memory.dump> linux.graphics.fbdev`
    - **说明**：可用于恢复图形界面数据（如屏幕截图）。

13. **`linux.hidden_modules.Hidden_modules`**
    - **功能**：通过内存雕刻查找隐藏的内核模块。
    - **用法**：`python3 vol.py -f <memory.dump> linux.hidden_modules`
    - **说明**：检测未在标准模块列表中显示的模块。

14. **`linux.iomem.IOMem`**
    - **功能**：生成类似 `/proc/iomem` 的 I/O 内存映射信息。
    - **用法**：`python3 vol.py -f <memory.dump> linux.iomem`
    - **说明**：分析硬件内存分配情况。

15. **`linux.ip.Addr`**
    - **功能**：列出所有网络接口的地址信息。
    - **用法**：`python3 vol.py -f <memory.dump> linux.ip.Addr`
    - **说明**：类似 `ip addr` 的输出，显示 IP 配置。

16. **`linux.ip.Link`**
    - **功能**：列出网络接口信息，类似 `ip link show`。
    - **用法**：`python3 vol.py -f <memory.dump> linux.ip.Link`
    - **说明**：提供接口状态和 MAC 地址等信息。

17. **`linux.kallsyms.Kallsyms`**
    - **功能**：枚举内核符号表（kallsyms）。
    - **用法**：`python3 vol.py -f <memory.dump> linux.kallsyms`
    - **说明**：提取内核函数和变量的符号信息。

18. **`linux.keyboard_notifiers.Keyboard_notifiers`**
    - **功能**：解析键盘通知链，检查是否被篡改。
    - **用法**：`python3 vol.py -f <memory.dump> linux.keyboard_notifiers`
    - **说明**：检测键盘记录器或钩子。

19. **`linux.kmsg.Kmsg`**
    - **功能**：读取内核日志缓冲区。
    - **用法**：`python3 vol.py -f <memory.dump> linux.kmsg`
    - **说明**：类似 `dmesg`，提取内核日志。

20. **`linux.kthreads.Kthreads`**
    - **功能**：枚举内核线程（kthread）函数。
    - **用法**：`python3 vol.py -f <memory.dump> linux.kthreads`
    - **说明**：分析内核级线程活动。

21. **`linux.library_list.LibraryList`**
    - **功能**：枚举进程加载的库。
    - **用法**：`python3 vol.py -f <memory.dump> linux.library_list`
    - **说明**：类似 `ldd`，显示动态链接库。

22. **`linux.lsmod.Lsmod`**
    - **功能**：列出已加载的内核模块。
    - **用法**：`python3 vol.py -f <memory.dump> linux.lsmod`
    - **说明**：提供模块名称、大小和地址。

23. **`linux.lsof.Lsof`**
    - **功能**：列出每个进程打开的文件。
    - **用法**：`python3 vol.py -f <memory.dump> linux.lsof`
    - **说明**：类似 `lsof` 命令，显示文件描述符。

24. **`linux.malfind.Malfind`**
    - **功能**：查找进程内存中可能包含注入代码的区域。
    - **用法**：`python3 vol.py -f <memory.dump> linux.malfind`
    - **说明**：检测恶意代码或内存注入。

25. **`linux.modxview.Modxview`**
    - **功能**：集中显示 `lsmod`、`check_modules` 和 `hidden_modules` 的结果。
    - **用法**：`python3 vol.py -f <memory.dump> linux.modxview`
    - **说明**：帮助快速发现模块异常。

26. **`linux.mountinfo.MountInfo`**
    - **功能**：列出进程挂载命名空间中的挂载点。
    - **用法**：`python3 vol.py -f <memory.dump> linux.mountinfo`
    - **说明**：分析挂载文件系统。

27. **`linux.netfilter.Netfilter`**
    - **功能**：列出 Netfilter 钩子。
    - **用法**：`python3 vol.py -f <memory.dump> linux.netfilter`
    - **说明**：检查网络过滤规则的修改。

28. **`linux.pagecache.Files`**
    - **功能**：列出页面缓存中的文件。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pagecache.Files`
    - **说明**：提取缓存中的文件数据。

29. **`linux.pagecache.InodePages`**
    - **功能**：列出并恢复缓存的 inode 页面。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pagecache.InodePages`
    - **说明**：恢复文件元数据。

30. **`linux.pagecache.RecoverFs`**
    - **功能**：将缓存的文件系统（目录、文件、符号链接）恢复为压缩 tarball。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pagecache.RecoverFs`
    - **说明**：重建文件系统结构。

31. **`linux.pidhashtable.PIDHashTable`**
    - **功能**：通过 PID 哈希表枚举进程。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pidhashtable`
    - **说明**：替代方法提取进程信息。

32. **`linux.proc.Maps`**
    - **功能**：列出所有进程的内存映射。
    - **用法**：`python3 vol.py -f <memory.dump> linux.proc.Maps [--pid=<PID>]`
    - **说明**：显示虚拟内存区域及其权限。

33. **`linux.psaux.PsAux`**
    - **功能**：列出进程及其命令行参数。
    - **用法**：`python3 vol.py -f <memory.dump> linux.psaux`
    - **说明**：类似 `ps aux`，提供详细进程信息。

34. **`linux.pscallstack.PsCallStack`**
    - **功能**：枚举每个任务的调用栈。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pscallstack`
    - **说明**：分析进程执行路径。

35. **`linux.pslist.PsList`**
    - **功能**：列出内存中的活动进程。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pslist`
    - **说明**：基础进程列表插件。

36. **`linux.psscan.PsScan`**
    - **功能**：扫描内存中的进程，包括隐藏或已终止的。
    - **用法**：`python3 vol.py -f <memory.dump> linux.psscan`
    - **说明**：比 `pslist` 更全面，可能有误报。

37. **`linux.pstree.PsTree`**
    - **功能**：以树形结构列出进程（基于父进程 ID）。
    - **用法**：`python3 vol.py -f <memory.dump> linux.pstree`
    - **说明**：展示进程层次关系。

38. **`linux.ptrace.Ptrace`**
    - **功能**：枚举 ptrace 的追踪者和被追踪任务。
    - **用法**：`python3 vol.py -f <memory.dump> linux.ptrace`
    - **说明**：检查调试或监控行为。

39. **`linux.sockstat.Sockstat`**
    - **功能**：列出所有进程的网络连接。
    - **用法**：`python3 vol.py -f <memory.dump> linux.sockstat`
    - **说明**：显示套接字信息。

40. **`linux.tracing.ftrace.CheckFtrace`**
    - **功能**：检测 ftrace 钩子。
    - **用法**：`python3 vol.py -f <memory.dump> linux.tracing.ftrace.CheckFtrace`
    - **说明**：检查内核追踪系统的篡改。

41. **`linux.tracing.perf_events.PerfEvents`**
    - **功能**：列出每个进程的性能事件。
    - **用法**：`python3 vol.py -f <memory.dump> linux.tracing.perf_events.PerfEvents`
    - **说明**：分析性能监控数据。

42. **`linux.tracing.tracepoints.CheckTracepoints`**
    - **功能**：检测 tracepoints 钩子。
    - **用法**：`python3 vol.py -f <memory.dump> linux.tracing.tracepoints.CheckTracepoints`
    - **说明**：检查内核追踪点的完整性。

43. **`linux.tty_check.tty_check`**
    - **功能**：检查 TTY 设备是否被钩子修改。
    - **用法**：`python3 vol.py -f <memory.dump> linux.tty_check`
    - **说明**：检测终端相关的恶意行为。

44. **`linux.vmaregexscan.VmaRegExScan`**
    - **功能**：使用正则表达式扫描所有任务的虚拟内存区域。
    - **用法**：`python3 vol.py -f <memory.dump> linux.vmaregexscan`
    - **说明**：查找特定模式的数据。

45. **`linux.vmayarascan.VmaYaraScan`**
    - **功能**：使用 Yara 规则扫描所有任务的虚拟内存区域。
    - **用法**：`python3 vol.py -f <memory.dump> linux.vmayarascan`
    - **说明**：检测已知恶意签名。

46. **`linux.vmcoreinfo.VMCoreInfo`**
    - **功能**：枚举 VMCoreInfo 表。
    - **用法**：`python3 vol.py -f <memory.dump> linux.vmcoreinfo`
    - **说明**：提取虚拟机核心信息。

### Windows 插件

1. **`windows.amcache.Amcache`**
   - **功能**：从 AmCache 中提取已执行应用程序的信息。
   - **用法**：`python3 vol.py -f <memory.dump> windows.amcache`
   - **说明**：分析应用程序执行历史。

2. **`windows.bigpools.BigPools`**
   - **功能**：列出大页面池。
   - **用法**：`python3 vol.py -f <memory.dump> windows.bigpools`
   - **说明**：检查内核内存分配。

3. **`windows.cachedump.Cachedump`**
   - **功能**：从内存中转储 LSA 密钥。
   - **用法**：`python3 vol.py -f <memory.dump> windows.cachedump`
   - **说明**：提取缓存的凭据。

4. **`windows.callbacks.Callbacks`**
   - **功能**：列出内核回调和通知例程。
   - **用法**：`python3 vol.py -f <memory.dump> windows.callbacks`
   - **说明**：检测内核级钩子。

5. **`windows.cmdline.CmdLine`**
   - **功能**：列出进程命令行参数。
   - **用法**：`python3 vol.py -f <memory.dump> windows.cmdline`
   - **说明**：显示进程启动时的完整命令。

6. **`windows.cmdscan.CmdScan`**
   - **功能**：查找 Windows 命令历史记录。
   - **用法**：`python3 vol.py -f <memory.dump> windows.cmdscan`
   - **说明**：恢复命令提示符历史。

7. **`windows.consoles.Consoles`**
   - **功能**：查找 Windows 控制台缓冲区。
   - **用法**：`python3 vol.py -f <memory.dump> windows.consoles`
   - **说明**：提取控制台输入输出数据。

8. **`windows.crashinfo.Crashinfo`**
   - **功能**：列出 Windows 崩溃转储信息。
   - **用法**：`python3 vol.py -f <memory.dump> windows.crashinfo`
   - **说明**：分析系统崩溃日志。

9. **`windows.debugregisters.DebugRegisters`**
   - **功能**：未明确说明，但通常用于检查调试寄存器。
   - **用法**：`python3 vol.py -f <memory.dump> windows.debugregisters`
   - **说明**：可能用于检测调试或反调试行为。

10. **`windows.deskscan.DeskScan`**
    - **功能**：扫描每个窗口站的桌面实例。
    - **用法**：`python3 vol.py -f <memory.dump> windows.deskscan`
    - **说明**：分析桌面对象。

11. **`windows.desktops.Desktops`**
    - **功能**：枚举每个窗口站的桌面实例。
    - **用法**：`python3 vol.py -f <memory.dump> windows.desktops`
    - **说明**：类似 `deskscan`，但更专注于枚举。

啰嗦了这么多，终于到最后一个 Windows 插件了！以下是剩余的 Windows 插件解释，我会加快速度，确保内容完整。

12. **`windows.devicetree.DeviceTree`**
    - **功能**：基于驱动程序和附加设备列出设备树。
    - **用法**：`python3 vol.py -f <memory.dump> windows.devicetree`
    - **说明**：展示硬件设备层级关系。

13. **`windows.direct_system_calls.DirectSystemCalls`**
    - **功能**：检测绕过 EDR 的直接系统调用技术。
    - **用法**：`python3 vol.py -f <memory.dump> windows.direct_system_calls`
    - **说明**：分析恶意软件逃避检测行为。

14. **`windows.dlllist.DllList`**
    - **功能**：列出加载的 DLL。
    - **用法**：`python3 vol.py -f <memory.dump> windows.dlllist`
    - **说明**：检查进程依赖的动态链接库。

15. **`windows.driverirp.DriverIrp`**
    - **功能**：列出驱动程序的 IRP（I/O 请求包）。
    - **用法**：`python3 vol.py -f <memory.dump> windows.driverirp`
    - **说明**：分析驱动程序的 I/O 操作。

16. **`windows.drivermodule.DriverModule`**
    - **功能**：检测是否有被 rootkit 隐藏的驱动。
    - **用法**：`python3 vol.py -f <memory.dump> windows.drivermodule`
    - **说明**：验证驱动完整性。

17. **`windows.driverscan.DriverScan`**
    - **功能**：扫描内存中的驱动程序。
    - **用法**：`python3 vol.py -f <memory.dump> windows.driverscan`
    - **说明**：查找潜在隐藏驱动。

18. **`windows.dumpfiles.DumpFiles`**
    - **功能**：从内存样本中转储缓存文件内容。
    - **用法**：`python3 vol.py -f <memory.dump> windows.dumpfiles`
    - **说明**：恢复文件数据。

19. **`windows.envars.Envars`**
    - **功能**：显示进程环境变量。
    - **用法**：`python3 vol.py -f <memory.dump> windows.envars`
    - **说明**：提取进程运行环境。

20. **`windows.filescan.FileScan`**
    - **功能**：扫描内存中的文件对象。
    - **用法**：`python3 vol.py -f <memory.dump> windows.filescan`
    - **说明**：查找文件相关数据结构。

21. **`windows.getservicesids.GetServiceSIDs`**
    - **功能**：列出进程令牌中的服务 SID。
    - **用法**：`python3 vol.py -f <memory.dump> windows.getservicesids`
    - **说明**：分析服务权限。

22. **`windows.getsids.GetSIDs`**
    - **功能**：打印每个进程拥有的 SID。
    - **用法**：`python3 vol.py -f <memory.dump> windows.getsids`
    - **说明**：检查用户和组标识。

23. **`windows.handles.Handles`**
    - **功能**：列出进程打开的句柄。
    - **用法**：`python3 vol.py -f <memory.dump> windows.handles`
    - **说明**：显示资源访问情况。

24. **`windows.hashdump.Hashdump`**
    - **功能**：从内存中转储用户哈希。
    - **用法**：`python3 vol.py -f <memory.dump> windows.hashdump`
    - **说明**：提取密码哈希。

25. **`windows.hollowprocesses.HollowProcesses`**
    - **功能**：列出被掏空的进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.hollowprocesses`
    - **说明**：检测进程掏空攻击。

26. **`windows.iat.IAT`**
    - **功能**：提取导入地址表（IAT），列出外部库使用的 API。
    - **用法**：`python3 vol.py -f <memory.dump> windows.iat`
    - **说明**：分析进程依赖的函数。

27. **`windows.indirect_system_calls.IndirectSystemCalls`**
    - **功能**：未明确说明，可能检测间接系统调用行为。
    - **用法**：`python3 vol.py -f <memory.dump> windows.indirect_system_calls`
    - **说明**：可能与恶意软件逃避技术相关。

28. **`windows.info.Info`**
    - **功能**：显示操作系统和内核详细信息。
    - **用法**：`python3 vol.py -f <memory.dump> windows.info`
    - **说明**：提供内存样本基本信息。

29. **`windows.joblinks.JobLinks`**
    - **功能**：打印进程作业链接信息。
    - **用法**：`python3 vol.py -f <memory.dump> windows.joblinks`
    - **说明**：分析进程分组。

30. **`windows.kpcrs.KPCRs`**
    - **功能**：打印每个处理器的 KPCR 结构。
    - **用法**：`python3 vol.py -f <memory.dump> windows.kpcrs`
    - **说明**：检查内核处理器控制区域。

31. **`windows.ldrmodules.LdrModules`**
    - **功能**：列出加载的模块。
    - **用法**：`python3 vol.py -f <memory.dump> windows.ldrmodules`
    - **说明**：类似 `dlllist`，但更全面。

32. **`windows.lsadump.Lsadump`**
    - **功能**：从内存中转储 LSA 密钥。
    - **用法**：`python3 vol.py -f <memory.dump> windows.lsadump`
    - **说明**：提取本地安全权限数据。

33. **`windows.malfind.Malfind`**
    - **功能**：查找可能包含注入代码的进程内存范围。
    - **用法**：`python3 vol.py -f <memory.dump> windows.malfind`
    - **说明**：检测恶意代码注入。

34. **`windows.mbrscan.MBRScan`**
    - **功能**：扫描并解析潜在的主引导记录（MBR）。
    - **用法**：`python3 vol.py -f <memory.dump> windows.mbrscan`
    - **说明**：检查引导扇区篡改。

35. **`windows.memmap.Memmap`**
    - **功能**：打印内存映射。
    - **用法**：`python3 vol.py -f <memory.dump> windows.memmap`
    - **说明**：显示进程内存布局。

36. **`windows.mftscan.ADS`**
    - **功能**：扫描 NTFS 的备用数据流（ADS）。
    - **用法**：`python3 vol.py -f <memory.dump> windows.mftscan.ADS`
    - **说明**：检测隐藏数据。

37. **`windows.mftscan.MFTScan`**
    - **功能**：扫描 MFT 文件对象。
    - **用法**：`python3 vol.py -f <memory.dump> windows.mftscan.MFTScan`
    - **说明**：分析 NTFS 文件系统元数据。

38. **`windows.mftscan.ResidentData`**
    - **功能**：扫描具有驻留数据的 MFT 记录。
    - **用法**：`python3 vol.py -f <memory.dump> windows.mftscan.ResidentData`
    - **说明**：恢复小型文件内容。

39. **`windows.modscan.ModScan`**
    - **功能**：扫描内存中的模块。
    - **用法**：`python3 vol.py -f <memory.dump> windows.modscan`
    - **说明**：查找隐藏模块。

40. **`windows.modules.Modules`**
    - **功能**：列出加载的内核模块。
    - **用法**：`python3 vol.py -f <memory.dump> windows.modules`
    - **说明**：类似 `lsmod`，但适用于 Windows。

41. **`windows.mutantscan.MutantScan`**
    - **功能**：扫描内存中的互斥对象。
    - **用法**：`python3 vol.py -f <memory.dump> windows.mutantscan`
    - **说明**：检查同步对象。

42. **`windows.netscan.NetScan`**
    - **功能**：扫描网络对象。
    - **用法**：`python3 vol.py -f <memory.dump> windows.netscan`
    - **说明**：提取网络连接数据。

43. **`windows.netstat.NetStat`**
    - **功能**：遍历网络跟踪结构。
    - **用法**：`python3 vol.py -f <memory.dump> windows.netstat`
    - **说明**：类似 `netstat`，显示网络状态。

44. **`windows.orphan_kernel_threads.Threads`**
    - **功能**：列出孤立内核线程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.orphan_kernel_threads.Threads`
    - **说明**：检测异常线程。

45. **`windows.pe_symbols.PESymbols`**
    - **功能**：打印进程和内核内存中 PE 文件的符号。
    - **用法**：`python3 vol.py -f <memory.dump> windows.pe_symbols`
    - **说明**：分析可执行文件符号表。

46. **`windows.pedump.PEDump`**
    - **功能**：从特定地址提取 PE 文件。
    - **用法**：`python3 vol.py -f <memory.dump> windows.pedump`
    - **说明**：恢复可执行文件。

47. **`windows.poolscanner.PoolScanner`**
    - **功能**：通用池扫描插件。
    - **用法**：`python3 vol.py -f <memory.dump> windows.poolscanner`
    - **说明**：扫描内核内存池。

48. **`windows.privileges.Privs`**
    - **功能**：列出进程令牌权限。
    - **用法**：`python3 vol.py -f <memory.dump> windows.privileges`
    - **说明**：检查特权使用情况。

49. **`windows.processghosting.ProcessGhosting`**
    - **功能**：列出标记为待删除或异常的进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.processghosting`
    - **说明**：检测进程隐藏技术。

50. **`windows.pslist.PsList`**
    - **功能**：列出内存中的进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.pslist`
    - **说明**：基础进程列表。

51. **`windows.psscan.PsScan`**
    - **功能**：扫描内存中的进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.psscan`
    - **说明**：包括隐藏进程。

52. **`windows.pstree.PsTree`**
    - **功能**：以树形结构列出进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.pstree`
    - **说明**：展示父子关系。

53. **`windows.psxview.PsXView`**
    - **功能**：通过多种方法列出进程，检测隐藏进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.psxview`
    - **说明**：基于《内存取证艺术》中的技术。

54. **`windows.registry.certificates.Certificates`**
    - **功能**：列出注册表中的证书存储。
    - **用法**：`python3 vol.py -f <memory.dump> windows.registry.certificates`
    - **说明**：提取证书信息。

55. **`windows.registry.getcellroutine.GetCellRoutine`**
    - **功能**：报告注册表 hive 中被钩住的 GetCellRoutine 处理程序。
    - **用法**：`python3 vol.py -f <memory.dump> windows.registry.getcellroutine`
    - **说明**：检测注册表篡改。

56. **`windows.registry.hivelist.HiveList`**
    - **功能**：列出内存中的注册表 hive。
    - **用法**：`python3 vol.py -f <memory.dump> windows.registry.hivelist`
    - **说明**：显示注册表结构。

57. **`windows.registry.hivescan.HiveScan`**
    - **功能**：扫描内存中的注册表 hive。
    - **用法**：`python3 vol.py -f <memory.dump> windows.registry.hivescan`
    - **说明**：查找隐藏 hive。

58. **`windows.registry.printkey.PrintKey`**
    - **功能**：列出 hive 或特定键下的注册表键。
    - **用法**：`python3 vol.py -f <memory.dump> windows.registry.printkey`
    - **说明**：提取注册表内容。

59. **`windows.registry.userassist.UserAssist`**
    - **功能**：打印 UserAssist 注册表键和信息。
    - **用法**：`python3 vol.py -f <memory.dump> windows.registry.userassist`
    - **说明**：分析用户活动记录。

60. **`windows.scheduled_tasks.ScheduledTasks`**
    - **功能**：解码注册表中的计划任务信息。
    - **用法**：`python3 vol.py -f <memory.dump> windows.scheduled_tasks`
    - **说明**：包括触发器、操作等。

61. **`windows.sessions.Sessions`**
    - **功能**：列出带有会话信息的进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.sessions`
    - **说明**：从环境变量提取会话数据。

62. **`windows.shimcachemem.ShimcacheMem`**
    - **功能**：从 ahcache.sys AVL 树读取 Shimcache 条目。
    - **用法**：`python3 vol.py -f <memory.dump> windows.shimcachemem`
    - **说明**：分析应用程序兼容性缓存。

63. **`windows.skeleton_key_check.Skeleton_Key_Check`**
    - **功能**：查找 Skeleton Key 恶意软件的迹象。
    - **用法**：`python3 vol.py -f <memory.dump> windows.skeleton_key_check`
    - **说明**：检测特定恶意行为。

64. **`windows.ssdt.SSDT`**
    - **功能**：列出系统服务描述符表。
    - **用法**：`python3 vol.py -f <memory.dump> windows.ssdt`
    - **说明**：检查系统调用表。

65. **`windows.statistics.Statistics`**
    - **功能**：列出内存空间统计信息。
    - **用法**：`python3 vol.py -f <memory.dump> windows.statistics`
    - **说明**：提供内存使用概况。

66. **`windows.strings.Strings`**
    - **功能**：读取 strings 命令输出并标识所属进程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.strings`
    - **说明**：关联字符串和进程。

67. **`windows.suspended_threads.SuspendedThreads`**
    - **功能**：枚举挂起的线程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.suspended_threads`
    - **说明**：检查异常线程状态。

68. **`windows.suspicious_threads.SuspiciousThreads`**
    - **功能**：列出可疑的用户态线程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.suspicious_threads`
    - **说明**：检测潜在恶意线程。

69. **`windows.svcdiff.SvcDiff`**
    - **功能**：比较列表遍历和扫描发现的服务，查找 rootkit。
    - **用法**：`python3 vol.py -f <memory.dump> windows.svcdiff`
    - **说明**：验证服务完整性。

70. **`windows.svclist.SvcList`**
    - **功能**：列出 services.exe 中的服务链表。
    - **用法**：`python3 vol.py -f <memory.dump> windows.svclist`
    - **说明**：显示服务信息。

71. **`windows.svcscan.SvcScan`**
    - **功能**：扫描 Windows 服务。
    - **用法**：`python3 vol.py -f <memory.dump> windows.svcscan`
    - **说明**：查找隐藏服务。

72. **`windows.symlinkscan.SymlinkScan`**
    - **功能**：扫描符号链接。
    - **用法**：`python3 vol.py -f <memory.dump> windows.symlinkscan`
    - **说明**：检查符号链接对象。

73. **`windows.thrdscan.ThrdScan`**
    - **功能**：扫描 Windows 线程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.thrdscan`
    - **说明**：提取线程信息。

74. **`windows.threads.Threads`**
    - **功能**：列出进程线程。
    - **用法**：`python3 vol.py -f <memory.dump> windows.threads`
    - **说明**：显示线程详情。

75. **`windows.timers.Timers`**
    - **功能**：打印内核定时器及相关模块 DPC。
    - **用法**：`python3 vol.py -f <memory.dump> windows.timers`
    - **说明**：检测恶意定时器。

76. **`windows.truecrypt.Passphrase`**
    - **功能**：查找 TrueCrypt 缓存的密码。
    - **用法**：`python3 vol.py -f <memory.dump> windows.truecrypt.Passphrase`
    - **说明**：恢复加密密码。

77. **`windows.unhooked_system_calls.unhooked_system_calls`**
    - **功能**：查找 Skeleton Key 恶意软件的迹象（重复功能？）。
    - **用法**：`python3 vol.py -f <memory.dump> windows.unhooked_system_calls`
    - **说明**：可能与 `skeleton_key_check` 类似。

78. **`windows.unloadedmodules.UnloadedModules`**
    - **功能**：列出卸载的内核模块。
    - **用法**：`python3 vol.py -f <memory.dump> windows.unloadedmodules`
    - **说明**：检查模块卸载历史。

79. **`windows.vadinfo.VadInfo`**
    - **功能**：列出进程内存范围（VAD）。
    - **用法**：`python3 vol.py -f <memory.dump> windows.vadinfo`
    - **说明**：分析虚拟地址描述符。

80. **`windows.vadregexscan.VadRegExScan`**
    - **功能**：使用正则表达式扫描 VAD 内存。
    - **用法**：`python3 vol.py -f <memory.dump> windows.vadregexscan`
    - **说明**：查找特定模式。

81. **`windows.vadwalk.VadWalk`**
    - **功能**：遍历 VAD 树。
    - **用法**：`python3 vol.py -f <memory.dump> windows.vadwalk`
    - **说明**：详细检查 VAD 结构。

82. **`windows.vadyarascan.VadYaraScan`**
    - **功能**：使用 Yara 规则扫描 VAD 内存。
    - **用法**：`python3 vol.py -f <memory.dump> windows.vadyarascan`
    - **说明**：检测已知恶意签名。

83. **`windows.verinfo.VerInfo`**
    - **功能**：列出 PE 文件的版本信息。
    - **用法**：`python3 vol.py -f <memory.dump> windows.verinfo`
    - **说明**：提取文件元数据。

84. **`windows.virtmap.VirtMap`**
    - **功能**：列出虚拟映射区域。
    - **用法**：`python3 vol.py -f <memory.dump> windows.virtmap`
    - **说明**：分析虚拟内存布局。

85. **`windows.windows.Windows`**
    - **功能**：枚举桌面实例的窗口。
    - **用法**：`python3 vol.py -f <memory.dump> windows.windows`
    - **说明**：检查 GUI 窗口信息。

86. **`windows.windowstations.WindowStations`**
    - **功能**：扫描顶级窗口站。
    - **用法**：`python3 vol.py -f <memory.dump> windows.windowstations`
    - **说明**：分析窗口站结构。

### macOS 插件

1. **`mac.bash.Bash`**
   - **功能**：从内存中恢复 Bash 命令历史。
   - **用法**：`python3 vol.py -f <memory.dump> mac.bash`
   - **说明**：类似 Linux 的 `bash` 插件，提取命令记录。

2. **`mac.check_syscall.Check_syscall`**
   - **功能**：检查系统调用表是否被钩子修改。
   - **用法**：`python3 vol.py -f <memory.dump> mac.check_syscall`
   - **说明**：检测 rootkit。

3. **`mac.check_sysctl.Check_sysctl`**
   - **功能**：检查 sysctl 处理程序是否被钩子修改。
   - **用法**：`python3 vol.py -f <memory.dump> mac.check_sysctl`
   - **说明**：验证内核参数完整性。

4. **`mac.check_trap_table.Check_trap_table`**
   - **功能**：检查 Mach 陷阱表是否被钩子修改。
   - **用法**：`python3 vol.py -f <memory.dump> mac.check_trap_table`
   - **说明**：检测 Mach 内核钩子。

5. **`mac.dmesg.Dmesg`**
   - **功能**：打印内核日志缓冲区。
   - **用法**：`python3 vol.py -f <memory.dump> mac.dmesg`
   - **说明**：类似 Linux 的 `kmsg`。

6. **`mac.ifconfig.Ifconfig`**
   - **功能**：列出所有设备的网络接口信息。
   - **用法**：`python3 vol.py -f <memory.dump> mac.ifconfig`
   - **说明**：类似 `ifconfig` 命令。

7. **`mac.kauth_listeners.Kauth_listeners`**
   - **功能**：列出 kauth 监听器及其状态。
   - **用法**：`python3 vol.py -f <memory.dump> mac.kauth_listeners`
   - **说明**：检查授权框架钩子。

8. **`mac.kauth_scopes.Kauth_scopes`**
   - **功能**：列出 kauth 范围及其状态。
   - **用法**：`python3 vol.py -f <memory.dump> mac.kauth_scopes`
   - **说明**：分析授权范围。

9. **`mac.kevents.Kevents`**
   - **功能**：列出进程注册的事件处理程序。
   - **用法**：`python3 vol.py -f <memory.dump> mac.kevents`
   - **说明**：检查内核事件监听。

10. **`mac.list_files.List_Files`**
    - **功能**：列出所有进程的打开文件描述符。
    - **用法**：`python3 vol.py -f <memory.dump> mac.list_files`
    - **说明**：类似 `lsof`。

11. **`mac.lsmod.Lsmod`**
    - **功能**：列出加载的内核模块。
    - **用法**：`python3 vol.py -f <memory.dump> mac.lsmod`
    - **说明**：显示内核扩展。

12. **`mac.lsof.Lsof`**
    - **功能**：列出所有进程的打开文件描述符。
    - **用法**：`python3 vol.py -f <memory.dump> mac.lsof`
    - **说明**：与 `list_files` 功能类似。

13. **`mac.malfind.Malfind`**
    - **功能**：查找可能包含注入代码的内存范围。
    - **用法**：`python3 vol.py -f <memory.dump> mac.malfind`
    - **说明**：检测恶意注入。

14. **`mac.mount.Mount`**
    - **功能**：列出挂载信息。
    - **用法**：`python3 vol.py -f <memory.dump> mac.mount`
    - **说明**：类似 `mount` 命令。

15. **`mac.netstat.Netstat`**
    - **功能**：列出所有进程的网络连接。
    - **用法**：`python3 vol.py -f <memory.dump> mac.netstat`
    - **说明**：类似 `netstat`。

16. **`mac.proc_maps.Maps`**
    - **功能**：列出进程内存范围。
    - **用法**：`python3 vol.py -f <memory.dump> mac.proc_maps`
    - **说明**：类似 `proc.Maps`。

17. **`mac.psaux.Psaux`**
    - **功能**：恢复程序命令行参数。
    - **用法**：`python3 vol.py -f <memory.dump> mac.psaux`
    - **说明**：类似 `ps aux`。

18. **`mac.pslist.PsList`**
    - **功能**：列出内存中的进程。
    - **用法**：`python3 vol.py -f <memory.dump> mac.pslist`
    - **说明**：基础进程列表。

19. **`mac.pstree.PsTree`**
    - **功能**：以树形结构列出进程。
    - **用法**：`python3 vol.py -f <memory.dump> mac.pstree`
    - **说明**：展示进程层级。

20. **`mac.socket_filters.Socket_filters`**
    - **功能**：枚举内核套接字过滤器。
    - **用法**：`python3 vol.py -f <memory.dump> mac.socket_filters`
    - **说明**：检查网络过滤。

21. **`mac.timers.Timers`**
    - **功能**：检查恶意内核定时器。
    - **用法**：`python3 vol.py -f <memory.dump> mac.timers`
    - **说明**：分析定时任务。

22. **`mac.trustedbsd.Trustedbsd`**
    - **功能**：检查恶意的 TrustedBSD 模块。
    - **用法**：`python3 vol.py -f <memory.dump> mac.trustedbsd`
    - **说明**：验证安全策略。

23. **`mac.vfsevents.VFSevents`**
    - **功能**：列出过滤文件系统事件的进程。
    - **用法**：`python3 vol.py -f <memory.dump> mac.vfsevents`
    - **说明**：检查文件系统监控。

---

### 注意事项

上述插件功能来自Jan 17发布的v2.11.0版本的vol3，若官方给出新的插件功能或对已有功能进行调整，后面会再更新

## **Volatility 2 插件列表**

### **进程与线程分析**

- `pslist` - 通过 `EPROCESS` 列表显示所有运行中的进程  
- `pstree` - 以树状结构显示进程列表  
- `psxview` - 通过多个方法检测隐藏进程  
- `psscan` - 通过内存扫描查找进程对象  
- `threads` - 分析 `_ETHREAD` 和 `_KTHREAD`  
- `thrdscan` - 线程对象的内存扫描  

### **内存映射与模块分析**

- `dlllist` - 列出每个进程加载的 DLL  
- `ldrmodules` - 检测未链接的 DLL  
- `modscan` - 通过内存扫描查找内核模块  
- `modules` - 显示已加载的内核模块  
- `memmap` - 显示进程的虚拟地址空间映射  
- `vadinfo` - 显示虚拟地址描述符 (VAD) 信息  
- `vadwalk` - 遍历 VAD 树  
- `vadtree` - 以树状结构显示 VAD  

### **网络分析**

- `connections` - 列出所有活动的网络连接（仅适用于 Windows XP/2003）  
- `connscan` - 通过内存扫描查找 TCP 连接  
- `sockets` - 显示所有开放的 socket 连接  
- `sockscan` - 通过内存扫描查找 socket 对象  

### **注册表分析**

- `hivelist` - 显示注册表 hives  
- `hivescan` - 通过内存扫描查找注册表 hive  
- `hivedump` - 导出注册表 hive 内容  
- `printkey` - 显示特定的注册表键及其子键和值  
- `shimcache` - 解析 Application Compatibility Shim Cache  
- `shellbags` - 显示 ShellBags 注册表信息  
- `auditpol` - 提取安全策略 (`HKLM\SECURITY\Policy\PolAdtEv`)  
- `getservicesids` - 获取注册表中服务的 SID  
- `shutdowntime` - 从注册表获取系统关闭时间  

### **文件系统分析**

- `filescan` - 通过内存扫描查找文件对象  
- `dumpfiles` - 提取映射到内存的文件  
- `mftparser` - 解析 NTFS 主文件表 (MFT)  
- `notepad` - 列出当前打开的 Notepad 文本内容  

### **进程注入与恶意代码分析**

- `malfind` - 查找隐藏和注入的代码  
- `apihooks` - 检测进程和内核中的 API Hook  
- `moddump` - 转储内核模块  
- `procdump` - 转储进程的可执行文件  
- `memdump` - 转储进程的整个地址空间  
- `dlldump` - 转储进程中的 DLL  
- `impscan` - 扫描进程调用的导入函数  
- `yarascan` - 使用 YARA 规则扫描进程或内核内存  

### **取证与事件日志分析**

- `evtlogs` - 提取 Windows 事件日志 (XP/2003)  
- `timeliner` - 从内存中的各种工件创建时间线  
- `cmdscan` - 解析命令行历史记录 (`_COMMAND_HISTORY`)  
- `consoles` - 解析 `_CONSOLE_INFORMATION` 结构体中的历史命令  
- `clipboard` - 提取 Windows 剪贴板内容  
- `iehistory` - 重建 Internet Explorer 缓存 / 历史记录  

### **用户活动分析**

- `getsids` - 显示进程的 SID 信息  
- `privs` - 显示进程权限  
- `userassist` - 解析 UserAssist 注册表项  
- `sessions` - 列出 `_MM_SESSION_SPACE` 详情（用户登录会话）  

### **内核分析**

- `ssdt` - 显示 SSDT (System Service Descriptor Table)  
- `idt` - 显示中断描述符表 (IDT)  
- `gdt` - 显示全局描述符表 (GDT)  
- `driverirp` - 检测驱动 IRP Hook  
- `driverscan` - 通过内存扫描查找驱动对象  
- `drivermodule` - 关联驱动对象到内核模块  
- `unloadedmodules` - 列出已卸载的内核模块  
- `kpcrscan` - 扫描 KPCR 结构体  

### **虚拟化分析**

- `qemuinfo` - 提取 QEMU 相关信息  
- `vboxinfo` - 提取 VirtualBox 相关信息  
- `vmwareinfo` - 提取 VMware VMSS/VMSN 相关信息  

### **加密与凭据**

- `cachedump` - 提取 Windows 缓存的域密码哈希  
- `hashdump` - 提取 LM/NTLM 哈希  
- `lsadump` - 提取 LSA 机密信息  
- `truecryptsummary` - 提取 TrueCrypt 信息  
- `truecryptpassphrase` - 查找 TrueCrypt 缓存的密码  
- `truecryptmaster` - 恢复 TrueCrypt 7.1a 主密钥  

### **图形界面与交互**

- `windows` - 显示桌面窗口信息  
- `screenshot` - 生成基于 GDI 的伪截图  
- `wndscan` - 通过内存扫描查找窗口对象  
- `deskscan` - 通过内存扫描查找桌面对象  

### **调试与数据提取**

- `imageinfo` - 识别内存镜像的基本信息  
- `imagecopy` - 将物理地址空间复制为 DD 镜像  
- `raw2dmp` - 将物理内存样本转换为 WinDBG 崩溃转储  
- `volshell` - 提供交互式的内存分析 shell  

### 注意事项

其实也没必要写了，因为vol2他们再没有更新过了，我这里写的是最后一版本的插件汇总了，然后得说明下使用方法

`python2 vol.py -f 1.mem --profile=xxxxx {plugins}`

对了，对于Linux还有一些拓展插件，这里我选择碰到了再补充,它们的路径在volatility/plugins/linux中，很多拓展插件呢

`linux_recover_filesystem --dump-dir=xxx/`可以恢复出这个镜像的所有文件（只能是可以恢复的）

> 这里有个小tip（可选）在我的设备中，我需要在root模式下开启虚拟环境，然后再使用这个命令，否则这个命令不能创建文件，导致失败

`linux_find_file -L` 可以列出所有文件

`linux_find_file -i <offset> -o xxx.date` 可以根据offset提取对应的文件

>> Yolo will be continuously updated.
