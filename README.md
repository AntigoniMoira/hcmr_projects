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

>The filters must be separated by &

1. equal : =
2. not equal : __ne
3. one of a list of values : __in
4. greater than or equal : __gte
5. greather than : __gt
6. less than or equal : __lte
7. less than : __lt
8. ilike : __icontains
9. ordering : ordering= e.g. `/api/platforms/?ordring=id` (ascending order) or  `/api/platforms/?ordring=-id` (descending order)
    >By default all data are sorted by id in an ascending order.
10. Row limiting : limit=
    >By adding &limit=# to an entity, the result set is limited and returns only the requested number of resources. 
11. Column Filtering: fields=
    >By using the "fields" keyword, the fields / columns that construct the resources can be defined.
    e.g `/api/platforms/?fields=id,inst,pi_name&limit=1` returns:
    ```json
	{
            "id": 1,
            "inst": 33,
            "pi_name": " "
        }
	```

### Available filters for each ULR

* #### `GET /api/platforms/?filters` :

    * ##### `id` : =, __ne, __in (e.g. `/api/platforms/?id__in=12,13,14`)
    * ##### `pid` : =, __ne, __in
    * ##### `tspr` : =, __ne
    * ##### `type` : =, __ne, __in
    * ##### `inst__id` : =, __in (e.g. `/api/platforms/?inst__id__in=1,2,3`)
    * ##### `dts` : __lt, __gt, __lte, __gte, icontains
    * ##### `dte` : __lt, __gt, __lte, __gte, icontains
    * ##### `lat` : __lt, __gt, __lte, __gte
    * ##### `lon` : __lt, __gt, __lte, __gte
    * ##### `status` : =true, =false
    * ##### `params` : __icontains
    * ##### `wmo` : =, __ne, __icontains
    * ##### `pi_name` : __icontains
    * ##### `assembly_center` : =, __ne, __in

* #### `GET /api/institutions/?filters` :

    * ##### `id` : =, __ne, __in 
    * ##### `name_native` : =, __ne, __icontains
    * ##### `abrv` : =, __ne, __in, __icontains
    * ##### `country` :=, __ne, __in, __icontains

* #### `GET /api/parameters/?filters` :

    * ##### `id` : =, __ne, __in 
    * ##### `pname` : =, __ne, __in, __icontains
    * ##### `unit` : =, __ne, __in, __icontains
    * ##### `long_name` : __icontains
    * ##### `stand_name` : =, __ne, __in, __icontains 
    * ##### `category_long` : =, __ne, __in, __icontains
    * ##### `category_short` : =, __ne, __in, __icontains

* #### `GET /api/<platform>/?filters` :

    * ##### `id` : =, __ne, __in 
    * ##### `dt` : __lt, __gt, __lte, __gte, __icontains
    * ##### `lat` : __lt, __gt, __lte, __gte
    * ##### `lon` : __lt, __gt, __lte, __gte 
    * ##### `posqc` : =, __ne, __in, __lt, __gt, __lte, __gte
    * ##### `pres` : __lt, __gt, __lte, __gte
    * ##### `presqc` : =, __ne, __in, __lt, __gt, __lte, __gte
    * ##### `param__id` : =, __ne, __in
    * ##### `val` : __lt, __gt, __lte, __gte
    * ##### `valqc` : =, __ne, __in, __lt, __gt, __lte, __gte

### Update DB

* #### `POST /api/<platform>/` :

It gets a json (example):

```json
	{
	"meta": [
		{
			"fval_qc": "-128",
			"fval": "-9999.99",
			"stand_name": "air_temperature",
			"long_name": "Air temperature in dry bulb",
			"init": "degrees_C",
			"pname": "DRYT"
		},
		{
			"fval_qc": "-128",
			"fval": "-9999.99",
			"stand_name": "eastward_sea_water_velocity",
			"long_name": "West-east current component",
			"init": "m s-1",
			"pname": "EWCT"
		}
    ],
	"data": [
		{
			"presqc": "1",
			"dvalqc": "0",
			"param": "DRYT",
			"val": "8.87",
			"posqc": "1",
			"lat": "45.5488",
			"valqc": "1",
			"dt": "2018-03-18 00:00:00",
			"lon": "13.5505",
			"pres": "-3.5"
		},
		{
			"presqc": "1",
			"dvalqc": "0",
			"param": "DRYT",
			"val": "8.83",
			"posqc": "1",
			"lat": "45.5488",
			"valqc": "1",
			"dt": "2018-03-18 00:30:00",
			"lon": "13.5505",
			"pres": "-3.5"
		}
    ]
}
	```

And returns:
