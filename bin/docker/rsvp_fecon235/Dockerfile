#  Dockerfile                                                  Date : 2016-10-25
#
# _______________|  Jupyter notebooks from fecon235 using Docker containers
#                   Computational data tools for FINANCIAL ECONOMICS
#                   https://hub.docker.com/r/rsvp/fecon235
#
#           Usage:  To BUILD this Dockerfile:
#                        $ docker build -t IMAGENAME -f Dockerfile .
#                   where the period implies current directory.
#
#        Examples:  To RUN the image:
#                        $ docker run -p 8888:8888 -it IMAGENAME
#                   which should yield a prompt, then as root:
#                        % nbstart
#                   and interact with browser at http://localhost:8888
#
#            Tips:  - Pull the latest git commits from /opt/rsvp/fecon235
#                   - Learn about data volumes to persist data.
#
#    Dependencies:  Docker images: continuumio/{anaconda,anaconda3}
#                          https://hub.docker.com/r/continuumio/anaconda
#                          https://hub.docker.com/r/continuumio/anaconda3
#                          The "3" indicates python3, else it is python2 based;
#                          see FROM line at Begin Script.
#                   Python code:  https://github.com/rsvp/fecon235
#
#  CHANGE LOG 
#  2016-10-25  Use own tagged base: rsvp/ana2-pd0181 for replication and tests.
#              Improve entry UI.  Change SHELL from sh to bash. 
#              Introduce REBUILD line to induce new clone of fecon235. 
#              Reorder commands to optimize for Docker's copy-on-write.
#  2016-10-09  First stable version produced rsvp/fecon:v4.16.0525

# _______________     ::  BEGIN  Script ::::::::::::::::::::::::::::::::::::::::

#  Tip: Obtain the base image in itself by, for example:
#       $ docker pull continuumio/anaconda:4.2.0
FROM rsvp/ana2-pd0181
#  The size of this image alone is just over 2 GB -- so patience.
#  We may switch to miniconda and install only needed packages.

MAINTAINER Adriano rsvp.github.com
#          Lead developer for fecon235


#      __________ SET-UP

SHELL ["/bin/bash", "-c"]
#  Other RUN will use /bin/sh as default (ugh!)

#  Update the repository sources:
#  RUN apt-get update
#  ... advisable before any apt-get installs for the Linux environment.

#  Make DIRECTORIES:  [Hassle of setting up an USER can be avoided.]
RUN mkdir -p /opt/rsvp/bin  /opt/rsvp/dock
#            /opt is designed for third-party software.

#  Set ENVIRONMENT variables for Bash and Python:
ENV PATH /opt/rsvp/bin:$PATH
ENV PYTHONPATH /opt/rsvp/bin:/opt/rsvp:$PYTHONPATH

#  conda is like pip for Python, but for anaconda* environments.
#  Use conda to INSTALL jupyter and other Python dependencies:
RUN /opt/conda/bin/conda install \
    jupyter \
    pandas-datareader \
    -y --quiet 


RUN echo " ::  REBUILD BELOW, marker: CHANGE THIS LINE: 2016-10-17 ::::::::"
#  Editing this line will induce new clone of fecon235.

#  Install fecon235 REPOSITORY from GitHub:
RUN cd /opt/rsvp && git clone https://github.com/rsvp/fecon235.git


#  Expose the traditional port for Jupyter notebook: 
#  EXPOSE 8888
#  ... we shall instead use "-p 8888:8888" at the command line instead.


#  Write NOTEBOOK START COMMAND as script:  [Using "alias" NOT advisable!] 
#
RUN echo '/opt/conda/bin/jupyter notebook --notebook-dir=/opt/rsvp/fecon235/nb \
          --ip="0.0.0.0" --port=8888 --no-browser' > /opt/rsvp/bin/nbstart     \
          &&  chmod 755 /opt/rsvp/bin/nbstart
#
#  DOES NOT WORK: --ip="127.0.0.1" OR --ip="localhost"
#  Jupyter docs use: --ip="0.0.0.0" which means all IPv4 addresses on local machine.
#  Using http://localhost:8888 on your browser should still work.
#
#  Anaconda usess: --ip="*" which generates stern security warnings, but it's for
#  Docker Machine VM which will interface at: http://<DOCKER-MACHINE-IP>:8888,


#  Set the MAIN command for this image:   [For TESTING command directly.] 
#  ENTRYPOINT /opt/conda/bin/jupyter notebook --notebook-dir=/opt/rsvp/fecon235/nb \
#             --ip="0.0.0.0" --port=8888 --no-browser 


#  Set the MAIN command for this image, with user instructions:
ENTRYPOINT cd /opt/rsvp/fecon235 \
   &&  echo ' PORT required:  $ docker run -p 8888:8888 -it rsvp/fecon235' \
   &&  echo ' '  \
   &&  echo ' ::  Welcome! Git repository cloned at:  /opt/rsvp/fecon235'  \
   &&  echo ' ::  Run "nbstart" for Jupyter notebooks, then interact with' \
   &&  echo ' ::                host browser at http://localhost:8888'     \
   &&  echo ' '  \
   &&  /bin/bash
#  ... should yield root prompt, all set for action, e.g. nbstart
#  (Using WORKDIR only scopes within a Dockerfile, not in a container.)

#  Specify default argument to Entrypoint:
#  CMD ['-c', 'nbstart']
#  ... fallback when an argument is not given on command line by user,
#      however, the container's Bash prompt will not be accessible
#      after the execution of 'nbstart'.
#  Note that only one CMD allowed per Dockerfile, and it can contain an 
#  absolute command (not taking an argument from the command line).


# _______________ EOS ::  END of Script ::::::::::::::::::::::::::::::::::::::::

#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=conf :
