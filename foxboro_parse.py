#%%
import pandas as pd
import re

#%%
foxboro_raw = 'raw_data/testdata.out'


with open(foxboro_raw, encoding='latin') as f:
    # patterns for Foxboro config files
    new_block_pattern = r'^NAME\s+=\s+(?P<compound>\w+):(?P<name>\w+)'
    block_param_pattern = r'\s+(?P<param>\w+)\s+=\s+(?P<value>.*)$'
    end_block_pattern = r'^END$'

    # Build a dictionary containing the data for a block
    blocks = {}
    block_dict = {}
    block_counter = 0
    for line in f:
        # Find a new block
        if name := re.search(new_block_pattern, line):
            block_dict['COMPOUND'] = name.group('compound')
            block_dict['NAME'] = name.group('name')

        # Find the block parameters
        elif block_param := re.search(block_param_pattern, line):
            param = block_param.group('param')
            value = block_param.group('value')
            block_dict[param] = value

        # At the end of a block add it to a dataframe
        elif end := re.search(end_block_pattern, line):
            block_type = block_dict['TYPE']
            block_df = pd.DataFrame(block_dict, index=[0])

            if block_type not in blocks:
                blocks[block_type] = block_df
            else:
                blocks[block_type] = pd.concat([blocks[block_type], block_df], ignore_index=True)
            
            # count the new block and reset 
            block_counter += 1
            block_dict = {}
    
    print(f'Gathered data for {block_counter} blocks')

#%%
