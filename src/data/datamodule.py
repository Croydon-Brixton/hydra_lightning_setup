from pytorch_lightning import LightningDataModule

from torch_geometric.loader import DataLoader
#from torch.loader import DataLoader # TODO Change if not using torch_geometric

from src.utils.transforms import get_transforms

class SampleDatamodule(pl.LightningDataModule):
    def __init__(self, data_dir: str = "path/to/dir",
                 batch_size: int = 32,
                 dataset_name: str = "sample_dataset",
                 transforms=None):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.dataset_name = dataset_name
        self.transforms = transforms
        
    def download(self):
        # Download data
        raise NotImplementedError("Download not implemented yet")
    

    def setup(self, stage: str):
    
        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            if self.dataset_name == 'sample_dataset':
                self.train_dataset, self.val_dataset = self.get_sample_dataset()
            if self.dataset_name == 'another_dataset':
                self.train_dataset, self.val_dataset = self.get_another_dataset()

        # Assign test dataset for use in dataloader(s)
        if stage == "test":
            #self.mnist_test = MNIST(self.data_dir, train=False, transform=self.transforms)
            raise NotImplementedError("Test stage not implemented yet")

        if stage == "predict":
            #self.mnist_predict = MNIST(self.data_dir, train=False, transform=self.transforms)
            raise NotImplementedError("Predict stage not implemented yet")
        
    def get_sample_dataset(self):
        train_dataset = SampleDataset(cfg)
        val_dataset = SampleDataset(cfg)
        return train_dataset, val_dataset
    
    def get_another_dataset(self):
        raise NotImplementedError("Another dataset not implemented yet")

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size)

    def predict_dataloader(self):
        return DataLoader(self.predict_dataset, batch_size=self.batch_size)

    def teardown(self, stage: str):
        # Used to clean-up when the run is finished
        raise NotImplementedError("Teardown not implemented yet")


def get_datamodule(cfg):
    """Return the datamodule based on the config."""
    
    transforms = get_transforms(cfg)
    
    datamodule = SampleDatamodule(data_dir=cfg.data_dir,
                                  batch_size=cfg.batch_size,
                                  dataset_name=cfg.dataset_name,
                                  transforms=transforms)
    
    return datamodule