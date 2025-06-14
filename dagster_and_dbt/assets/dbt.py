import dagster as dg
from dagster import AssetKey
from dagster_dbt import dbt_assets, DbtCliResource, DagsterDbtTranslator

from dagster_and_dbt.project import dbt_project
class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return dg.AssetKey(f"taxi_{name}")
        else:
            return super().get_asset_key(dbt_resource_props)

        
@dbt_assets(
    manifest=dbt_project.manifest_path, 
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
)
def dbt_analytics(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


