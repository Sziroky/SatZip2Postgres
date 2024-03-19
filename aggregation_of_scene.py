import pandas as pd
import os

def s2_merge_images_per_scene(ext_output):
    df = pd.read_csv(ext_output)
    pivoted = df.pivot_table(index='scene_id', columns='band', values='path', aggfunc='first').reset_index()
    merged = df.merge(pivoted, on='scene_id')
    aggregated = merged.groupby('scene_id').agg('first').reset_index()
    return aggregated.drop(['band', 'path'], axis=1).to_csv(os.path.abspath(ext_output),index= False)

def s1_merge_images_per_scene(ext_output):
    df = pd.read_csv(ext_output)
    pivoted = df.pivot_table(index='scene_id', columns='code', values='path', aggfunc='first').reset_index()
    merged = df.merge(pivoted, on='scene_id')
    aggregated = merged.groupby('scene_id').agg('first').reset_index()
    return aggregated.drop(['path'], axis=1).to_csv(os.path.abspath(ext_output),index= False)