import passiveGenerator

mode = 'item'
checkMode = 'all'

if checkMode == 'all':
    passiveGenerator.errorCheck(mode)
elif checkMode == 'single':
    print(passiveGenerator.printPassives(passiveGenerator.nameToID("47214",mode),mode))