# Copyright (c) SURF
# Copyright (c) Caspar van Leeuwen
# Distributed under the terms of GNU GPLv3 license

"""
The classes defined here expand upon the the batchspawner package (https://github.com/jupyterhub/batchspawner).
The CustomSlurmSpawner allows a fully customizable version of the batchspawner.slurmspawner.
Customization occurs through a web form.
The items of the web form dropdown menus are populated by querying the batch system through scontrol.
"""

# import asyncio
# from async_generator import async_generator, yield_, yield_from_
# import pwd
# import os
# import re
# import sys
# 
# import xml.etree.ElementTree as ET
# 
# from jinja2 import Template
# 
# from tornado import gen
# from tornado.process import Subprocess
# from subprocess import CalledProcessError
# from tornado.iostream import StreamClosedError
# 
# from jupyterhub.spawner import Spawner
# from jupyterhub.traitlets import Command
from traitlets import (
     Unicode, default
)
# 
# from jupyterhub.utils import random_port
# from jupyterhub.spawner import set_user_setuid
# import jupyterhub
from batchspawner import SlurmSpawner
from textwrap import dedent
import subprocess

# def format_template(template, *args, **kwargs):
#     """Format a template, either using jinja2 or str.format().
# 
#     Use jinja2 if the template is a jinja2.Template, or contains '{{' or
#     '{%'.  Otherwise, use str.format() for backwards compatability with
#     old scripts (but you can't mix them).
#     """
#     if isinstance(template, Template):
#         return template.render(*args, **kwargs)
#     elif '{{' in template or '{%' in template:
#         return Template(template).render(*args, **kwargs)
#     return template.format(*args, **kwargs)

class CustomSlurmSpawner(SlurmSpawner):
    # Some utility variables
    reservation = ""

    # Some utility functions
    def query_reservations(self):
        result = subprocess.check_output(["scontrol", "show", "reservation", "--oneliner"]).decode('UTF-8')
        reservations = [""]
        for line in result.split("\n"):
            columns = line.split()
            for column in columns:
                key, value = column.split("=", 1)
                if key == "ReservationName":
                    reservations.append(value)
                    break
        self.log.info("Reservations found: %s" % reservations)
        return reservations

    def query_partitions(self):
        # result = subprocess.check_output(["sudo", "-H", "-u", "casparl", "bash", "-c", "'scontrol", "show", "partitions", "--oneliner'"]).decode('UTF-8')
        result = subprocess.check_output(["scontrol", "show", "partitions", "--oneliner"]).decode('UTF-8')
        partitions = [""]
        for line in result.split("\n"):
            columns = line.split()
            for column in columns:
                key, value = column.split("=", 1)
                if key == "PartitionName":
                    partitions.append(value)
                    break
        self.log.info("Partitions found: %s" % partitions)
        return partitions

    def options_form(self, spawner):

        form = ""

        # Number of cores
        form += dedent("""
        <label for="cores">Cores:</label>
        <input class="form-control" type="number" name="cores" min="1" max="16" value="2" required autofocus>
        """)

        # Time limit
        form += dedent("""
        <label for="time">Time Limit:</label>
        <input class="form-control" type="number" name="time" min="10" max="240" value="30" step="10" required autofocus>
        """)

        # Partitions
        form += dedent("""
        <label for="partition">Partition:</label>
        <select class="form-control" name="partition" autofocus>
        """)

        partitions = self.query_partitions()
        for partition in partitions:
            form += """<option value="{}">{}</option>""".format(partition, partition)

        form += dedent("""
        </select>
        """)

        # Reservation
        form += dedent("""
        <label for="reservation">Reservation:</label>
        <select class="form-control" name="reservation" autofocus>
        """)

        reservations = self.query_reservations()
        for reservation in reservations:
            form += """<option value="{}">{}</option>""".format(reservation, reservation)

        form += dedent("""
        </select>
        """)

        return form

    def options_from_form(self, formdata):
        options = dict()

        # Reservation:
        options["reservation"] = formdata["reservation"][0]
        # If non-empty reservation, create #SBATCH line with reservation.
        # This allows the user to select NO reservation, without creating a dangling "#SBATCH --reservation" in the job script.
        if options["reservation"]:
            options["reservation"] = "#SBATCH --reservation %s" % options["reservation"]

        # Others
        options["partition"] = formdata["partition"][0]
        options["cores"] = formdata["cores"][0]
        options["time"] = formdata["time"][0]
        return options

#    batch_script_string = "#!/bin/bash\n"
#    batch_script_string += """#SBATCH -p {partition}
#{reservation}
##SBATCH -t {time}
##SBATCH -n {cores}
##SBATCH -J jupyterhub-singleuser
###SBATCH -e "/scratch/jupyterhub-%j.out"
###SBATCH -o "/scratch/jupyterhub-%j.out"
##SBATCH -e "/home/{username}/jupyterhub-%j.out"
##SBATCH -o "/home/{username}/jupyterhub-%j.out"
##SBATCH --uid {username}
##SBATCH --get-user-env
##SBATCH --chdir /home/{username}
#
#module load 2019
#module load jupyterhub/1.0.0-foss-2018b-Python-3.6.6
#module load IRkernel/1.0.2-foss-2018b-R-3.5.1-Python-3.6.6
#echo "Loading jupyterlmod..."
#module load jupyterlmod/1.7.5-foss-2018b-Python-3.6.6
#echo "Jupyterlmod loaded!"
#
#jupyter nbextension install --py jupyterlmod --user
#jupyter nbextension enable --py jupyterlmod --user
#jupyter serverextension enable --py jupyterlmod --user
#
## Pretty ugly, but need to export explicitly for now... (it is not in the PATH upon login, so can't do a 'which' on it)
#export LMOD_CMD=/hpc/eb/modules-4.0.0/libexec/modulecmd.tcl
#
##module load ErasmusCourse/1.0-foss-2018b-R-3.5.1
##module load cuDNN/7.6.3-CUDA-10.0.130
#
#echo "Starting notebook server..."
#{cmd}
#"""
#    batch_script = Unicode(batch_script_string).tag(config=False)
