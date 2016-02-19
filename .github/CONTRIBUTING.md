# CONTRIBUTING: Notes on forks and pull requests

We are thrilled that you would like to collaborate on 
this project. Your help is essential.

- Code revisions: please kindly follow [Github flow]. 

- Running tests: details are in the `tests` directory. 
  Python tests will run under both py.test and nosetests.

- For integration testing, we run all notebooks in batch mode 
  in a Linux environment. This also syncs temporary notebooks 
  with current data.

- If you have modified code in a Jupyter/IPython notebook where 
  there are many embedded images, *please clear out all 
  outputs before your commit*. (The only exception arises 
  in the case of major releases where we want archival 
  samples of images generated).


## Submitting a pull request

0. [Fork][fork] and clone the repository.
0. Create a new branch: `git checkout -b my-branch-name`
0. Make your change, add tests, and make sure the tests still pass.
0. Be sure to ***pull origin/master and rebase*** before the next step.
0. Push to your fork and [submit a pull request][pr]
0. Kindly wait for your pull request to be reviewed.
0. Stay in touch with fellow developers at [Gitter].


## Tips regarding pull requests

- Refine tests whenever possible.

- Update documentation as necessary.  

- Keep your change focused. If there are multiple changes that are not
  dependent upon each other, please submit them as separate pull requests.

- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).


**Thank you very much for your consideration. 
Your contributing work is very appreciated.**


## Resources

- [Contributing to Open Source on GitHub](https://guides.github.com/activities/contributing-to-open-source/)
- [Using Pull Requests](https://help.github.com/articles/using-pull-requests/)


- - - -

Revision date : 2016-01-23

[fork]:         https://github.com/rsvp/fecon235/fork "Fork fecon235"
[Github flow]:  http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
[Gitter]:       https://gitter.im/rsvp/fecon235 "Gitter fecon235"
[pr]:           https://github.com/rsvp/fecon235/compare "Pull request"
