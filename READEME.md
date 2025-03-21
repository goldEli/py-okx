
```
 python -m unittest tests/test_strategy.py
```

```
pip freeze > requirements.txt
```
```
pip install -r requirements.txt
```

```
nohup python -u index.py > output.log 2>&1 &
ps aux | grep index.py
tail -f output.log
```

# Test

```
python -m unittest tests/test__is_top_upper_strategy.py
python -m unittest tests/test__is_normal_upper_strategy.py
python -m unittest tests/test__is_bottom_lower_strategy.py
python -m unittest tests/test__is_normal_lower_strategy.py
```

```
python -m unittest discover tests
```
