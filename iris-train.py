import argparse
import keepsake

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

import torch
from torch import nn
from torch.autograd import Variable

def train(learning_rate, num_epochs):
    # Create an "experiment". This represents a run of your training script.
    # It saves the training code at the given path and any hyperparameters.
    experiment = keepsake.init(
        path='.',
        params={
            'learning_rate': learning_rate,
            'num_epochs': num_epochs,    
        },
    )

    print('Downloading data set...')

    iris = load_iris()
    train_X, valid_X, train_y, valid_y = train_test_split(
        iris.data,
        iris.target,
        train_size=0.8,
        test_size=0.2,
        random_state=0,
        stratify=iris.target,
    )
    train_X = torch.FloatTensor(train_X)
    valid_X = torch.FloatTensor(valid_X)
    train_y = torch.LongTensor(train_y)
    valid_y = torch.LongTensor(valid_y)

    print('Define a model')
    torch.manual_seed(0)
    model = nn.Sequential(
        nn.Linear(4, 15),
        nn.ReLU(),
        nn.Linear(15, 3),
    )
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=learning_rate,
    )
    criterion = nn.CrossEntropyLoss()

    print('Train...')
    for epoch in range(num_epochs):
        model.train()
        optimizer.zero_grad()
        outputs = model(train_X)
        loss = criterion(outputs, train_y)
        loss.backward()
        optimizer.step()

        with torch.no_grad():
            model.eval()
            output = model(valid_X)
            acc = (output.argmax(1) == valid_y)\
                .float().sum() / len(valid_y)
        print(f'Epoch {epoch}, train loss: {loss.item():.3f}, validation accuracy: {acc:.3f}')
        torch.save(model, 'model.pth')

        # Create a checkpoint within the experiment.
        # This saves the metrics at that point, and makes a copy of the file
        # or directory given, which could weights and any other artifacts.
        experiment.checkpoint(
            path='model.pth',
            step=epoch,
            metrics={'loss': loss.item(), 'accuracy': acc},
            primary_metric=('loss', 'minimize'),
        )

if __name__ == '__main__':
    # Set arguments from commandline
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, default=0.01)
    parser.add_argument('--num_epochs', type=int, default=100)
    args = parser.parse_args()

    # Train
    train(args.learning_rate, args.num_epochs)