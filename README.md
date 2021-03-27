### Trial Keepsake

### How to use
#### Install dependencies
```bash
pipenv install
```

#### Run training code 2 times
```bash
pipenv shell
python iris-train.py
python iris-train.py --learning_rate=0.2
```

#### Experiments and checkpoints
The calls to the `keepsake` Python library have saved your experiments locally.
You can use `keepsake ls` to list them:
```bash
keepsake ls
```
The `--filter` flag allows you to narrow in on a subset of experiments:
```bash
keepsake ls --filter 'learning_rate = 0.2'
```
Within experiments are **checkpoints**, which are created every time you call `experiment.checkpoint()` in `iris-train.py`.
To list the checkpoints within an experiment, you can use `keepsake show`:
```bash
keepsake show <an experiment ID>
```
You can also use `keepsake show` on a checkpoint to get all the information about it:
```bash
keepsake show <a checkpoint ID>
```
Let's copare the last checkpoints from the two experiments we ran:
```bash
keepsake diff <the last checkpoint ID in the first experimen> <the last checkpoint ID in the second experiment>
```
The `keepsake checkout` command will copy the code and weights from a checkpoint into your working directory:
```bash
keepsake checkout <a checkpoint ID>
```
