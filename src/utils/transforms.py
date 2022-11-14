from torch_geometric.data import Data

class ExampleTransform(object):
    
    def __init__(self, cfg):
        pass
    
    def __call__(self, data : Data) -> Data:
        
        ## Do some transformation here
        
        return data


def get_transforms(cfg):
    
    transforms = []
    
    if 'example_transform' in cfg.transforms:
        transforms.append(ExampleTransform(cfg))
    
    return transforms