# HKUBE local python api 

api implementation for running  and debbuging hkubes pipeline without installing hkube 

## prerequisite 

 - install hkubectl 
  ```bash
# Check release page for latest version
os = "linux/macos/windows"
curl -Lo hkubectl https://github.com/kube-HPC/hkubectl/releases/download/$(curl -s https://api.github.com/repos/kube-HPC/hkubectl/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')/hkubectl-{linux/macos/windows} \
&& chmod +x hkubectl \
&& sudo mv hkubectl /usr/local/bin/
```
-  run ``hkubectl dry-run start``

- run `pip install hkube.debbuging-python-api`

## usage 

```python 
import asyncio
from hkube_debbuging_python_api.builder import Builder


def test1(data):
    print(data['input'])
    return data['input']


class runBuilder():

    async def run():
        build = Builder()
        pipe = await build.createPipeline("test")
        pipe.algorithm("test").input(5).add(test1).algorithm(
            'test2').input("@test").add(test1).execute()


bla = asyncio.run(runBuilder.run())
print('finish')

```
