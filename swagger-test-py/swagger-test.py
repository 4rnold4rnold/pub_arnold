import warnings
warnings.filterwarnings("ignore")



import os
import requests
import urllib3
from urllib.request import getproxies
from swagger_parser import SwaggerParser
import swagger2
from openapi3 import OpenAPI
import json


# SSL 검증 비활성화
urllib3.disable_warnings()

def download_swagger(url, directory, file_name):
    # 디렉토리가 없으면 생성
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 파일 경로
    file_path = os.path.join(directory, file_name)

    # 파일이 존재하면 삭제
    if os.path.exists(file_path):
        os.remove(file_path)

    # 시스템 프록시 가져오기
    proxies = getproxies()

    # 다운로드
    response = requests.get(url, proxies=proxies, verify=False)
    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"파일이 다운로드되었습니다: {file_path}")
    return file_path

#https://github.com/Dorthu/openapi3
def parse_json_openapi_v3(file_path):


    result = False
    summary = ""

    # load the spec file and read the JSON
    with open(file_path) as f:
        spec = json.load(f)

    # parse the spec into python - this will raise if the spec is invalid
    api = OpenAPI(spec)

    info = api.info["description"]
    print(info)
    summary += "== server description == \n{}".format(info)

    summary += "\n== api list =="

    return result, summary



# pyyml 버전이 langchain 과 버전 호환성이 맞지 않아 swagger-parser 를 이용하는 방식은 제외함
def parse_json_swagger_v2(file_path):
    summary = 'Here is the description of a services and information for each API.\n'

    parser = None

    try:
        parser = SwaggerParser(swagger_path=file_path)
    except Exception as e:
        return False, 'Error parsing Swagger file: {}'.format(str(e))

    info = parser.specification["info"]["description"]
    print(info)
    summary += "server description : \n{}".format(info)

    for operation in parser.operation:
        print(operation)
        summary += "\n{}: ".format(operation)

        path = parser.operation[operation][0]
        method = parser.operation[operation][1]
        tag = parser.operation[operation][2]

        print(path)
        # print(method)

        summary += "Path is \'{}\'".format(path)

        basepath = parser.specification["basePath"]
        modpath = path.replace(basepath, "")

        desc = ""
        if path in parser.specification["paths"]:
            desc = parser.specification["paths"][path][method]['summary']
        elif modpath in parser.specification["paths"]:
            desc = parser.specification["paths"][modpath][method]['summary']
        else:
            desc = ''

        print(desc)
        summary += " and description is \'{}\'.".format(desc)

    print(summary)
    return True, summary

#https://pypi.org/project/swagger2/
def parse_json_swagger2_v2(file_path):
    summary = 'Here is the description of a services and information for each API.\n'

    parser = None

    # 시스템 프록시 가져오기
    proxies = getproxies()

    try:
        parser = swagger2.parse(url=file_path, proxies=proxies, verify=False)

        info = parser.source["info"]["description"]
        print(info)
        summary += "== server description == \n{}".format(info)

        summary += "\n== api list =="
        for api in parser.apis:
            print(api.get('name'))
            summary += "\n{}: ".format(api.get('name'))

            path = api.get('path')
            method = api.get('method')

            print(path)
            # print(method)

            summary += "Path is \'{}\'".format(path)

            orgbasepath = parser.basePath
            modpath = path.replace(orgbasepath, "")

            desc = ""
            if path in parser.source["paths"]:
                desc = parser.source["paths"][path][method]['summary']
            elif modpath in parser.source["paths"]:
                desc = parser.source["paths"][modpath][method]['summary']
            else:
                desc = ''

            print(desc)
            summary += " and description is \'{}\'.".format(desc)

        print(summary)
        return True, summary

    except Exception as e:
        return False, 'Error parsing Swagger file: {}'.format(str(e))


def main():
    # URL 및 파일 경로
    url = "https://petstore.swagger.io/v2/swagger.json"
    # url = "https://petstore3.swagger.io/api/v3/openapi.json"

    directory = "swagger"
    file_name = "swagger.json"

    # swagger 파싱
    # parse_json_swagger_v2(r"swagger\swagger.json")

    # result, summary = parse_json_swagger_v2(file_path)
    isSwaggerV2 = True
    result, summary = parse_json_swagger2_v2(url)

    if result == False:
        print(summary)
        isSwaggerV2 = False

    if isSwaggerV2 == False :
        # swagger 다운로드 및 경로 가져오기
        file_path = download_swagger(url, directory, file_name)
        result, summary = parse_json_openapi_v3(file_path)



if __name__ == "__main__":
    main()
