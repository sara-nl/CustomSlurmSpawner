# CustomSlurmSpawner

This package provides a fully customizable SLURM spawner for Jupyterhub by deriving from batchspawner.SlurmSpawner and implementing an options_form. The elements in the options form are populated by querying the system with ```scontrol show XXX``` commands.
