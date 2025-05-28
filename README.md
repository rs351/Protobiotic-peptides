This notebook is a simple combination of the ProteinMPNN and Alphafold2 colab notebooks which permits the generation of 
protein sequences constrained by limited amino acid libraries, such as one might find available in protobiotic/astrobiological
environments (meteorites, protobiotic chemistry experiments, etc.). The additional Python code sweeps through folder trees
containing simulating protein structures and computes three structural comparions metrics: the TM-score, the RMSD and the
MaxSub-score. The respective C++ codes for computing these metrics can be found at:\\
https://zhanggroup.org/TM-align/ \\
https://zhanggroup.org/TM-score/  
