# PortScan
基于python3实现的端口扫描工具

## 依赖
- [x] python3+

### 使用说明

- 单端口扫描：

 ```python
python scan.py -i 127.0.0.1 -p 80
```
- 多端口扫描：

 ```python
python scan.py -i 127.0.0.1 -p 80,443,8080,8443,10250
```
- 扫描连续端口：

 ```python
python scan.py -i 127.0.0.1 -p 22-81
```
