# Ideal Status

Ideal Status is a platform to manage your websites status.


## Installation

After all, you need to create your environment and config your configuration file:

```bash
pip3 install venv
```

```bash
python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt
```

```bash
cp .env.default .env
```
Then set your secret key in `.env`

```python
SECRET_KEY=
```

Now you need to create the database using sqlite3, run the following commands:
```bash
flask shell
```

```python
db.create_all()
exit()
```

To start the app, run the following command:
```bash
flask --app app run
```

To deactivate your enviroment run the following command:
```bash
deactivate
```

## License
[MIT](https://mit-license.org/)
