# HCMR_POSEIDON

## Git flow (if you want to use it)
The basic idea is that the develop branch is your stage/dev branch/environment and the master branch is the production/live code currently running. 

1. Install git flow locally from [here](https://github.com/nvie/gitflow/wiki/Installation).
2. Create a develop branch locally. (if you haven't got one)
3. Run `git flow init` on your local repo. (press `Enter` on every step)
4. Keep develop and master branch updated locally.
5. Each time you need to create a new feature (or anything else) you run `git flow feature start some-name` command and a new feature branch is automatically created from the develop branch.
6. Develop your feature
7. Run `git pull origin develop` to make sure that you are up to date with the develop branch. If there are any conflicts, resolve, git add, and git commit again.
8. Run `git push origin feature/some-name` to upload you branch to the repository.
9. Then you go on [github](https://github.com/AntigoniMoira/hcmr_repository) and open a new pull request from the feature branch you just pushed to the develop branch and add reviewers.
10. If the reviewers approve the pull request you merge it and if you want you open a new pull request to master branch and follow the same process.
11. In case of a bugfix (if you want to fix something that is currently on production/live) you run `git flow bufix start some-name` and follow the same process, except now you merge with master and if everything is ok you merge with develop too.
12. When the feature/bugfix are completed you delete the branch and pull the latest develop/master changes.

More on git flow [here](https://github.com/nvie/gitflow) or [here](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).

## API URLS

### The following filters are available:

>1. equal : =
2. not equal : ne
3. one of a list of values : in
4. greater than or equal : gte
5. greather than : gt
6. less than or equal : lte
7. less than : lt
8. ilike : icontains

* ### `GET /api/platforms/?filters` :

    * #### `id` : =, __ne, __in (e.g. `/api/platforms/?id__in=12,13,14`)
    * #### `pid` : =, __ne, __in
    * #### `tspr` : =, __ne
    * #### `type` : =, __ne, __in
    * #### `inst__id` : =, __in (e.g. `/api/platforms/?inst__id__in=1,2,3`)
    * #### `dts` : lt, gt, lte, gte, icontains
    * #### `dte` : lt, gt, lte, gte, icontains
    * #### `lat` : lt, gt, lte, gte
    * #### `lon` : lt, gt, lte, gte
    * #### `status` : =true, =false
    * #### `params` : __icontains
    * #### `platform_code` : =, __ne
    * #### `wmo` : =, __ne, __icontains
    * #### `pi_name` : __icontains
    * #### `assembly_center` : =, __ne, __in

