from server import apis
def initialize_routes(api):
    # 脚本接口请求
    api.add_resource(apis.ExecuteController, '/data_factory/execute_method')
    api.add_resource(apis.GetFolderTree, '/data_factory/get_foler_tree')
    api.add_resource(apis.GetListByPath, '/data_factory/get_list_by_path')
    api.add_resource(apis.GetEnvironmentList, '/data_factory/get_env_list')
    api.add_resource(apis.Health, '/data_factory/Health')