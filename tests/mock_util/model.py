import os
import json
import uuid
import boto3
import random
import string
from decimal import Decimal
from datetime import datetime, timedelta
from faker import Faker
from typing import Dict, List, Union, Optional, Literal


class MockUtil:
    @staticmethod
    def get_mock_company_data(
        id: str = str(uuid.uuid4()),
        root_user_id: str = str(uuid.uuid4()),
        areas_de_atuacao: list = [
            "OEM",
            "CORE",
            "DEVICES",
            "AUDIT",
            "ACCEPTANCE",
            "ACCESS",
            "SUBSCRIBER",
        ],
    ) -> dict:
        fake: Faker = Faker()
        address = fake.address()
        name = fake.name()
        email = fake.email()
        alias = fake.text()
        phone = "+" + str(fake.random_number(13))
        return {
            "id": id,
            "sort_key": "companies",
            "company_id": "companies",
            "apikey": "G4akqkzDoM9eqYsGWUXBq5Eb8d3u3To52WHZNjRl",
            "apikey_identifier": "k7c85k2gk3",
            "usuario_raiz_id": root_user_id,
            "status": "ACTIVE",
            "frontend_osp": None,
            "uses_external_client": False,
            "sortable_field": f"{name} {id}",
            "searchable_address": address.lower(),
            "osp_version": "1.5",
            "address": address,
            "searchable_alias": alias.lower(),
            "integracao": {"osp_sync_endpoint": fake.url()[:-1].split("//")[1]},
            "areas_de_atuacao": areas_de_atuacao,
            "email": email,
            "name": name,
            "alias": alias,
            "searchable_name": name.lower(),
            "cnpj": "00000000000009",
            "phone": phone,
            "secondary_sort_key": "G4akqkzDoM9eqYsGWUXBq5Eb8d3u3To52WHZNjRl",
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": int(datetime.now().timestamp()),
            "datetime_updated": int(datetime.now().timestamp()),
        }

    @staticmethod
    def get_mock_resource_entity_data(
        name: str = None,
        code: str = None,
        read_resources: List[str] = [],
        write_resources: List[str] = [],
        delete_batch: List[str] = [],
    ) -> dict:
        fake: Faker = Faker()
        module = "oem"

        if name is None:
            name = fake.word()

        if code is None:
            code = fake.word()[:4]

        return {
            "id": f"resource_entities#{module}#{name}",
            "sort_key": "resource_entities",
            "name": name,
            "code": code,
            "module": module,
            "read_resources": read_resources,
            "write_resources": write_resources,
            "delete_batch": delete_batch,
        }

    @staticmethod
    def get_mock_integration_resource_entity_data(
        module: str = "osp", version: str = "1.5", roles: List[str] = []
    ) -> dict:
        return {
            "id": f"{module}#permissions#{version}",
            "sort_key": f"resource_entities#{module}",
            "version": version,
            "roles": roles,
        }

    @staticmethod
    def get_mock_request_map_data(
        name: str, methods: Dict[str, str], module: str = "oem"
    ) -> dict:
        lambda_name = f"fkw-iot-{module}-env-{name}"

        return {
            "id": f"request_map#{lambda_name}",
            "sort_key": "request_maps",
            "name": name,
            "lambda": lambda_name,
            "module": module,
            "paths": list(methods.values()),
            "methods": methods,
        }

    @staticmethod
    def get_mock_admin_plans(
        id: str = str(uuid.uuid4()), user: str = str(uuid.uuid4())
    ) -> dict:
        fake: Faker = Faker()

        name = random.choice(["BASIC", "STARTER", "EXTRA", "DELUXE"])

        price = random.choice([100.00, 150.00, 200.00, 300.00])

        dateAux = "{} {}".format(fake.date_between("-1d"), fake.time())

        services = random.choice(
            [
                ["service 01", "service 02", "service 03"],
                ["service 03", "service 04", "service 05"],
                ["service 03", "service 02"],
                ["service 01", "service 02", "service 03", "service 05"],
            ]
        )

        fields = {
            "fields_01": fake.word(),
            "fields_02": fake.word(),
            "fields_03": fake.word(),
        }
        status = random.choice(["ACTIVE", "INACTIVE"])
        company_type = random.choice(["Agro", "Health", "Telecom"])
        description = fake.text()

        return {
            "id": id,
            "name": name,
            "price": price,
            "services": services,
            "fields": fields,
            "status": status,
            "company_type": company_type,
            "created_by": user,
            "updated_by": user,
            "datetime_created": dateAux,
            "datetime_updated": dateAux,
            "description": description,
        }

    @staticmethod
    def get_mock_project_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        name: str = None,
        description: str = None,
        sql: bool = False,
        osp_id: str = None,
        utc: int = -3.0,
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.word()
        if description is None:
            description = fake.text()

        if sql:
            return {
                "id": id,
                "company_id": company_id,
                "name": name,
                "description": description,
                "created_by": str(uuid.uuid4()),
                "updated_by": str(uuid.uuid4()),
                "datetime_created": "{} {}".format(
                    fake.date_between("-1y"), fake.time()
                ),
                "datetime_updated": "{} {}".format(
                    fake.date_between("-1y"), fake.time()
                ),
                "osp_id": osp_id,
                "utc": utc,
            }

        return {
            "id": id,
            "sort_key": f"projects#{company_id}",
            "name": name,
            "searchable_name": name.lower(),
            "description": description,
            "searchable_description": description.lower(),
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "osp_id": fake.pyint(),
            "coords_reference": "-3.758630915878198,-38.48350524989656",
            "main_inventory_project": str(uuid.uuid4()),
            "main_inventory_project_name": "test",
            "corrective_threshold": 10,
            "auto_maintenance_enabled": False,
            "has_main_inventory": True,
            "utc": Decimal(utc),
        }

    @staticmethod
    def get_mock_role_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        resource_entities: Dict[str, str] = {},
        integration_resource_entities: Dict[str, any] = {},
    ) -> dict:
        fake: Faker = Faker()
        name = fake.word()
        description = fake.text()

        return {
            "id": id,
            "sort_key": f"roles#{company_id}" if company_id is not None else "roles",
            "resource_entities": resource_entities,
            "integration_resource_entities": integration_resource_entities,
            "name": name,
            "searchable_name": name.lower(),
            "description": description,
            "searchable_description": description.lower(),
            "status": "ACTIVE",
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
        }

    @staticmethod
    def get_mock_activity(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project_id: str = str(uuid.uuid4()),
        component_id: str = str(uuid.uuid4()),
        technician_id: str = str(uuid.uuid4()),
        responsible_id: str = str(uuid.uuid4()),
        activity: Literal[
            "DELAYED_MAINTENANCE", "DELAYED_ATTENDANCE", "DELAYED_ACCEPTANCE"
        ] = "DELAYED_MAINTENANCE",
        datetime_started: datetime = datetime.utcnow() - timedelta(hours=3),
        datetime_estimated_end: datetime = datetime.utcnow() + timedelta(hours=3),
        status: str = "OPEN",
        reason: str = None,
    ) -> dict:

        fake: Faker = Faker()

        if not reason:
            reason = fake.word()

        return {
            "id": id,
            "company_id": company_id,
            "project_id": project_id,
            "component_id": component_id,
            "technician_id": technician_id,
            "responsible_id": responsible_id,
            "activity": activity,
            "datetime_started": datetime_started,
            "datetime_estimated_end": datetime_estimated_end,
            "status": status,
            "reason": reason,
        }

    @staticmethod
    def get_mock_notification(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        name: str = str(uuid.uuid4()),
        channels: list[str] = ["WEB", "TELEGRAM", "SMS", "EMAIL"],
        projects: list[str] = [str(uuid.uuid4()), str(uuid.uuid4())],
        active: bool = True,
        sound_setting: Literal["SILENT", "AUDIBLE", "PERSISTENT"] = "SILENT",
        notification_type: Literal[
            "DELAYED_MAINTENANCE", "LOW_INVENTORY"
        ] = "DELAYED_MAINTENANCE",
        users: list[str] = [str(uuid.uuid4()), str(uuid.uuid4())],
        created_by: str = str(uuid.uuid4()),
        updated_by: str = str(uuid.uuid4()),
        datetime_created: datetime = datetime.utcnow() - timedelta(hours=3),
        datetime_updated: datetime = datetime.utcnow() + timedelta(hours=3),
        dynamo_db_entity: bool = False,
    ) -> dict:

        fake: Faker = Faker()

        if not name:
            name = fake.word()

        sort_key = f"notifications#{company_id}#{notification_type}"

        if dynamo_db_entity:
            datetime_created = int(datetime_created.timestamp())
            datetime_updated = int(datetime_updated.timestamp())

        return {
            "id": id,
            "sort_key": sort_key,
            "company_id": company_id,
            "name": name,
            "searchable_name": name.lower(),
            "active": active,
            "sound_setting": sound_setting,
            "channels": channels,
            "projects": projects,
            "notification_type": notification_type,
            "users": users,
            "created_by": created_by,
            "updated_by": updated_by,
            "datetime_created": datetime_created,
            "datetime_updated": datetime_updated,
        }

    @staticmethod
    def get_mock_notification_event(
        notification_type: str = "DELAYED_MAINTENANCE",
        company_id: str = str(uuid.uuid4()),
        project_name: str = None,
        project_id: str = str(uuid.uuid4()),
        component_name: str = None,
        status: Literal["OPEN", "IN_PROGRESS", "REVOKED", "ON_APPROVAL"] = "OPEN",
        reason: str = None,
        responsible_name: str = None,
        technician_name: str = None,
        datetime_started: datetime = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S"),
        datetime_estimated_end: datetime = datetime.utcnow().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
    ) -> dict:

        fake: Faker = Faker()

        if not project_name:
            project_name = fake.word()

        if not component_name:
            component_name = fake.word()

        if not reason:
            reason = fake.word()

        if not responsible_name:
            responsible_name = fake.name()

        if not technician_name:
            technician_name = fake.name()

        return {
            "notification_type": notification_type,
            "company_id": company_id,
            "project_name": project_name,
            "project_id": project_id,
            "component_name": component_name,
            "status": status,
            "reason": reason,
            "responsible_name": responsible_name,
            "technician_name": technician_name,
            "datetime_started": datetime_started,
            "datetime_estimated_end": datetime_estimated_end,
        }

    @staticmethod
    def get_mock_admin_announcement(
        id: str = str(uuid.uuid4()),
        sent: bool = False,
        duration: str = "2",
        companies: List[str] = [str(uuid.uuid4()), str(uuid.uuid4())],
        datetime_sent: datetime = None,
        datetime_start: datetime = None,
    ) -> dict:

        fake = Faker()

        subject = fake.word()
        message = fake.text()
        subject_en = fake.word()
        message_en = fake.text()
        subject_es = fake.word()
        message_es = fake.text()
        type = "custom"

        return {
            "id": id,
            "companies": companies,
            "subject": subject,
            "message": message,
            "subject_en": subject_en,
            "message_en": message_en,
            "subject_es": subject_es,
            "message_es": message_es,
            "sent": sent,
            "type": type,
            "duration": duration,
            "datetime_sent": datetime_sent,
            "datetime_start": datetime_start,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
        }

    @staticmethod
    def get_mock_user_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        permission: str = str(uuid.uuid4()),
        projects: List[str] = None,
        language: Literal["pt-BR", "en-US", "es-ES"] = None,
        push_web_token: str = None,
        telegram_id: str = None,
        email: str = None,
    ) -> dict:
        if projects is None:
            projects = [str(uuid.uuid4()), str(uuid.uuid4())]

        fake = Faker()
        name = fake.name()
        family_name = fake.last_name()
        if email is None:
            email = fake.email()
        phone_number = "+" + str(fake.random_number(13))

        if not language:
            languages = ["pt-BR", "en-US", "es-ES"]
            language = random.choice(languages)

        if not push_web_token:
            push_web_token = "cXusPS_A57m1Ym8LWh2pyr:APA91bHtDaUJXeVj8lrSGs1VWagywHDv79l2YCp869KF1rIkpKqal45vfdHrVxYK-TMAbkCdAL2pH-qbJMq9lZ2YeoCvhu4TJoNkBbdnBDLpPr8rsIyBzbZd0eQFgiZAB-xjll6Vj8WC"

        if not telegram_id:
            telegram_id = "1282515543"

        return {
            "id": id,  # "cf1cf44f-a61c-4041-8cd0-f17e8d3e07e9",
            "sort_key": f"users#{company_id}",
            "company_id": company_id,
            "searchable_family_name": family_name.lower(),
            "function_tag": [],
            "projects": projects,
            "status": "CONFIRMED",
            "hierarchy": "primary",
            "family_name": family_name,
            "email": email,
            "name": name,
            "telegram_id": telegram_id,
            "enabled": 1,
            "searchable_name": name.lower(),
            "push_mobile_token": None,
            "push_web_token": push_web_token,
            "language": language,
            "phone_number": phone_number,
            "permission": permission,
            "sortable_field": f"João Luiz {id}",
            "imagem_path": f"{company_id}/usuarios/{id}.png",
        }

    @staticmethod
    def get_mock_user_data_sql(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        updated_by: str = str(uuid.uuid4()),
        user_data: dict = None,
    ) -> dict:
        fake = Faker()
        name = fake.name()
        family_name = fake.last_name()
        email = fake.email()
        data = user_data or [name, family_name, email]

        return {
            "id": id,  # "cf1cf44f-a61c-4041-8cd0-f17e8d3e07e9",
            "company_id": company_id,
            "email": email,
            "name": name,
            "user_data": data,
            "created_by": created_by,
            "updated_by": updated_by,
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1y"), fake.time()),
        }

    @staticmethod
    def get_mock_maintenance_data(
        id: str,
        type: str = "CORRECTIVE",
        status: str = "OPEN",
        component_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        updated_by: str = str(uuid.uuid4()),
        datetime_created: datetime = datetime.utcnow() + timedelta(hours=-3),
        datetime_start: datetime = datetime.utcnow() - timedelta(hours=3),
        datetime_end: datetime = datetime.utcnow() + timedelta(hours=3),
        technician_id: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()
        technician_name = fake.name()
        technician_email = fake.email()
        reason = fake.word()

        return {
            "id": id,
            "technician_name": technician_name,
            "technician_email": technician_email,
            "technician_id": technician_id,
            "type": type,
            "status": status,
            "device_id": component_id,
            "company_id": company_id,
            "created_by": created_by,
            "updated_by": updated_by,
            "project": project,
            "associated_technicians_ids": [technician_id],
            "datetime_created": datetime_created,
            "datetime_finished": datetime_created,
            "datetime_departured": datetime_created,
            "datetime_arrived": datetime_created,
            "datetime_read": datetime_created,
            "datetime_start": datetime_start,
            "datetime_end": datetime_end,
            "reason": reason,
            # "datetime_started": datetime_created,
            "datetime_approved": datetime_created,
        }

    @staticmethod
    def get_mock_acceptance_data(
        id: str,
        status: str = "OPEN",
        component_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        updated_by: str = str(uuid.uuid4()),
        technician_id: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()
        technician_name = fake.name()
        technician_email = fake.email()

        return {
            "id": id,
            "technician_name": technician_name,
            "technician_email": technician_email,
            "technician_id": technician_id,
            "status": status,
            "device_id": component_id,
            "company_id": company_id,
            "created_by": created_by,
            "updated_by": updated_by,
            "project": project,
            "associated_technicians_ids": [technician_id],
            "additional_technicians_ids": [],
        }

    @staticmethod
    def create_dynamodb_core_table(table_name: str, region: str):
        conn = boto3.client("dynamodb", region_name=region)
        conn.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "sort_key", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "sort_key", "AttributeType": "S"},
                {"AttributeName": "secondary_sort_key", "AttributeType": "S"},
                {"AttributeName": "sortable_field", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "EntityIndex",
                    "KeySchema": [
                        {"AttributeName": "sort_key", "KeyType": "HASH"},
                        {"AttributeName": "id", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "SecondaryEntityIndex",
                    "KeySchema": [
                        {"AttributeName": "secondary_sort_key", "KeyType": "HASH"},
                        {"AttributeName": "id", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "SortableIndex",
                    "KeySchema": [
                        {"AttributeName": "sort_key", "KeyType": "HASH"},
                        {"AttributeName": "sortable_field", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
            ],
        )

    @staticmethod
    def create_dynamodb_integration_table(table_name: str, region: str):
        conn = boto3.client("dynamodb", region_name=region)
        conn.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "sort_key", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "sort_key", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "EntityIndex",
                    "KeySchema": [
                        {"AttributeName": "sort_key", "KeyType": "HASH"},
                        {"AttributeName": "id", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                }
            ],
        )

    @staticmethod
    def create_dynamodb_log_table(table_name: str, region: str):
        conn = boto3.client("dynamodb", region_name=region)
        conn.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},
                {"AttributeName": "sort_key", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "sort_key", "AttributeType": "S"},
                {"AttributeName": "new_status", "AttributeType": "S"},
                {"AttributeName": "datetime_created", "AttributeType": "N"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "EntityIndex",
                    "KeySchema": [
                        {"AttributeName": "sort_key", "KeyType": "HASH"},
                        {"AttributeName": "id", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "DatetimeCreation",
                    "KeySchema": [
                        {"AttributeName": "sort_key", "KeyType": "HASH"},
                        {"AttributeName": "datetime_created", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "NewStatusVariationIndex",
                    "KeySchema": [
                        {"AttributeName": "sort_key", "KeyType": "HASH"},
                        {"AttributeName": "new_status", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
            ],
        )

    @staticmethod
    def populate_data_into_dynamodb(table_name: str, region: str, item_data: dict):
        dynamodb = boto3.resource("dynamodb", region)
        table = dynamodb.Table(table_name)
        table.put_item(Item=item_data)

    @staticmethod
    def mock_user_data(
        company_id: str,
        id: str = "cf1cf44f-a61c-4041-8cd0-f17e8d3e07e9",
        permission: str = "b824923e-9caa-4bb2-94c5-51bdf9140108",
        language: Literal["pt-BR", "en-US", "es-ES"] = "pt-BR",
    ) -> dict:
        """
        Generate a fake mocked user data
        """

        fake = Faker()
        tenancies = [str(uuid.uuid4()), company_id, str(uuid.uuid4())]
        areas = {}
        permissions = {}
        for tenant in tenancies:
            permissions[tenant] = str(uuid.uuid4())
            areas[tenant] = [
                "OEM",
                "CORE",
                "DEVICES",
                "AUDIT",
                "ACCEPTANCE",
                "ACCESS",
                "SUBSCRIBER",
            ]
        permissions[company_id] = permission

        if not language:
            languages = ["pt-BR", "en-US", "es-ES"]
            language = random.choice(languages)

        return {
            "id": id,
            "name": fake.name(),
            "family_name": fake.last_name(),
            "phone_number": "+" + str(fake.random_number(13)),
            "language": language,
            "email": fake.email(),
            "company_id": company_id,
            "tenancies": tenancies,
            "permission": permissions,
            "areas": areas,
        }

    @staticmethod
    def mock_user_attributes(
        name: str,
        family_name: str,
        email: str,
        phone_number: str,
        language: str,
        company_id: str,
        tenancies: list,
        permission: dict,
        areas: dict,
        accepted_terms: str,
        id: str = None,
    ) -> list:
        """
        Generate a fake mocked atributtes list of user for cognito UserAttributes comparation
        """

        attributes = [
            {"Name": "name", "Value": name},
            {"Name": "family_name", "Value": family_name},
            {"Name": "email", "Value": email},
            {"Name": "phone_number", "Value": phone_number},
            {"Name": "custom:areas_de_atuacao", "Value": json.dumps(areas)},
            {"Name": "email_verified", "Value": "true"},
            {"Name": "custom:empresa", "Value": company_id},
            {"Name": "phone_number_verified", "Value": "true"},
            {"Name": "custom:permission", "Value": json.dumps(permission)},
            {"Name": "custom:accepted_terms", "Value": accepted_terms},
            {"Name": "custom:tenancies", "Value": json.dumps(tenancies)},
            {"Name": "custom:imagem_path", "Value": f"{company_id}/usuarios/{id}.png"},
            {"Name": "custom:language", "Value": language},
        ]

        if id:
            attributes.append({"Name": "sub", "Value": id})

        return attributes

    @staticmethod
    def get_mock_base64_image():
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{current_path}/image_base64_file.txt") as json_file:
            return json_file.read()

    @staticmethod
    def get_mock_authorize_event(type: str = "HTTP") -> dict:
        filename = "mock_auth_event.json"
        if type == "WEBSOCKET":
            filename = "mock_auth_websocket_event.json"
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{current_path}/{filename}") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_mock_proxy_event() -> dict:
        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(f"{current_path}/mock_proxy_event.json") as json_file:
            return json.load(json_file)

    @staticmethod
    def get_mock_audit_record(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = None,
    ) -> dict:
        fake = Faker()
        entity_type = fake.word()
        entity_id = fake.word()
        module = fake.word()
        method = fake.word()
        identificator_key = fake.word()
        identificator_value = fake.word()
        user_id = fake.word()
        user_name = fake.name() + " " + fake.last_name()
        user_email = fake.email()
        old_data = {"id": identificator_value, "value": "old"}
        new_data = {"id": identificator_value, "value": "new"}
        return {
            "id": id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "module": module,
            "method": method,
            "identificator_key": identificator_key,
            "identificator_value": identificator_value,
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "old_data": old_data,
            "new_data": new_data,
            "datetime_log": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "company_id": company_id,
        }

    @staticmethod
    def get_mock_chat(
        id: str = str(uuid.uuid4()),
        entity_id: str = str(uuid.uuid4()),
        entity_code: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        status: str = "PENDING",
        type: str = "MAINTENANCE",
        technician_id: str = str(uuid.uuid4()),
        user_id: str = str(uuid.uuid4()),
        title: str = "Mock title",
        is_dynamo: bool = False,
    ) -> dict:
        fake = Faker()
        datetime_created = "{} {}".format(fake.date_between("-1d"), fake.time())
        mock_entity = {
            "id": id,
            "title": title,
            "entity_id": entity_id,
            "entity_code": entity_code,
            "company_id": company_id,
            "project": project,
            "status": status,
            "user_status": "NOTIFIED" if status != "PENDING" else "READ",
            "technician_status": "READ" if status != "PENDING" else "NOTIFIED",
            "type": type,
            "last_message_author_id": technician_id,
            "last_message": fake.text(),
            "technician_id": technician_id,
            "user_id": user_id if status != "PENDING" else None,
            "created_by": technician_id,
            "updated_by": technician_id,
            "datetime_created": datetime_created,
            "datetime_updated": datetime_created,
        }

        if is_dynamo:
            timestamp_seconds = int(
                datetime.timestamp(
                    datetime.strptime(datetime_created, "%Y-%m-%d %H:%M:%S")
                )
            )
            mock_entity["searchable_title"] = mock_entity["title"].lower()
            mock_entity["datetime_created"] = timestamp_seconds
            mock_entity["datetime_updated"] = timestamp_seconds
            mock_entity["sort_key"] = f"chats#{company_id}"
            mock_entity["sortable_field"] = f"{timestamp_seconds} {id}"

        return mock_entity

    @staticmethod
    def get_mock_chat_message(
        id: str = str(uuid.uuid4()),
        chat_id: str = str(uuid.uuid4()),
        author_id: str = str(uuid.uuid4()),
        author_name: str = None,
        author_email: str = None,
        type: str = "TEXT",
        company_id: str = str(uuid.uuid4()),
        message: str = None,
        is_dynamo: bool = False,
        datetime_created: str = None,
        datetime_read: str = None,
    ) -> dict:
        fake = Faker()
        message = fake.text() if message is None else message
        author_name = fake.name() if author_name is None else author_name
        author_email = fake.email() if author_email is None else author_email
        datetime_created = (
            "{} {}".format(fake.date_between("-1d"), fake.time())
            if datetime_created is None
            else datetime_created
        )
        mock_entity = {
            "id": id,
            "message": message,
            "chat_id": chat_id,
            "author_id": author_id,
            "author_name": author_name,
            "author_email": author_email,
            "author_image": f"{company_id}/usuarios/{author_id}.png",
            "type": type,
            "company_id": company_id,
            "created_by": author_id,
            "datetime_created": datetime_created,
            "datetime_read": datetime_read,
        }

        if is_dynamo:
            timestamp_seconds = int(
                datetime.timestamp(
                    datetime.strptime(datetime_created, "%Y-%m-%d %H:%M:%S")
                )
            )
            mock_entity["datetime_created"] = timestamp_seconds
            mock_entity["sort_key"] = f"chat_messages#{company_id}#{chat_id}"
            mock_entity["sortable_field"] = f"{timestamp_seconds} {id}"

            if datetime_read is not None:
                mock_entity["datetime_read"] = timestamp_seconds

        return mock_entity

    @staticmethod
    def get_mock_chat_connection(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        user_id: str = str(uuid.uuid4()),
        created_date: str = (datetime.now() - timedelta(hours=3)).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    ):
        fake = Faker()
        return {
            "id": id,
            "sort_key": f"chat_ws_connections#{company_id}",
            "endpoint_url": fake.url(),
            "user_id": user_id,
            "company_id": company_id,
            "created_date": created_date,
            "context": {
                "routeKey": "$connect",
                "authorizer": {
                    "permissions": json.dumps(
                        {company_id: "42327367-1300-404c-b198-782bf19e9400"}
                    ),
                    "tenancies": json.dumps([company_id]),
                    "name": fake.name(),
                    "principalId": user_id,
                    "phone_number": "+5512341234123",
                    "integrationLatency": 319,
                    "id": user_id,
                    "imagem_path": "",
                    "family_name": fake.last_name(),
                    "email": fake.email(),
                },
            },
            "user_type": "USER",
            "secondary_sort_key": f"chat_ws_connections#{company_id}#{user_id}",
        }

    @staticmethod
    def get_mock_technician(
        id: str = str(uuid.uuid4()),
        name: str = None,
        family_name: str = None,
        email: str = None,
        company_id: str = str(uuid.uuid4()),
        phone_number: int = None,
    ) -> dict:
        fake = Faker()
        mobile = "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            for _ in range(100)
        )
        if not phone_number:
            phone_number = random.randint(10000000000, 90000000000)

        return {
            "id": id,
            "name": fake.name() if name is None else name,
            "family_name": fake.last_name() if family_name is None else family_name,
            "email": fake.email() if email is None else email,
            "company_id": company_id,
            "push_mobile_token": mobile,
            "phone_number": f"+55{phone_number}",
        }

    @staticmethod
    def get_technician_team_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        description: str = None,
        company_id: str = str(uuid.uuid4()),
        workshift_id: str = str(uuid.uuid4()),
        projects: str = [str(uuid.uuid4())],
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.name()
        if description is None:
            description = fake.text()

        return {
            "id": id,
            "name": name,
            "description": description,
            "workshift_id": workshift_id,
            "projects": projects,
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": "{} {}".format(fake.date_between("-1d"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1d"), fake.time()),
        }

    @staticmethod
    def get_accredited_company_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        company_id: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.name()

        created_by = str(uuid.uuid4())
        datetime_created = "{} {}".format(fake.date_between("-1d"), fake.time())
        return {
            "id": id,
            "name": name,
            "company_id": company_id,
            "created_by": created_by,
            "updated_by": created_by,
            "datetime_created": datetime_created,
            "datetime_updated": datetime_created,
        }

    @staticmethod
    def get_term_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        description: str = None,
        company_id: str = "SYS_FURUKAWA",
        language: Literal["pt_br", "en_us", "es_es"] = "pt_br",
        datetime_created: datetime = datetime.now(),
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.name()

        if description is None:
            description = fake.text()

        if language is None:
            language = "pt_br"

        return {
            "id": id,
            "name": name,
            "description": description,
            "language": language,
            "file_path": company_id + "/users/" + id + ".pdf",
            "company_id": company_id,
            "datetime_created": datetime_created,
        }

    @staticmethod
    def get_term_accept_log_data(
        id: str = str(uuid.uuid4()),
        user_id: str = str(uuid.uuid4()),
        term_id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        datetime_accepted: datetime = datetime.now(),
    ) -> dict:

        return {
            "id": id,
            "user_id": user_id,
            "term_id": term_id,
            "language": "pt_br",
            "company_id": company_id,
            "datetime_accepted": datetime_accepted,
        }

    @staticmethod
    def get_workshift_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        company_id: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()

        if name is None:
            name = fake.word()

        days = ["quarta"]
        schedules = [
            {
                "days": ["quarta"],
                "timestamp_end": "18:59",
                "timestamp_start": "00:00",
                "utc_offset": -3,
            }
        ]
        return {
            "id": id,
            "name": name,
            "days": days,
            "schedules": schedules,
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": "{} {}".format(fake.date_between("-1d"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1d"), fake.time()),
        }

    @staticmethod
    def get_work_shift_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        company_id: str = str(uuid.uuid4()),
        teams_to_add: str = str(uuid.uuid4()),
        teams_to_remove: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()
        fake.items
        fake.items
        return {
            "id": id,
            "name": name if name is not None else fake.word(),
            "days": [
                "domingo",
                "segunda",
                "sabado",
                "quinta",
                "sexta",
                "terca",
                "quarta",
            ],
            "schedules": [
                {
                    "days": ["segunda", "terca", "quarta", "quinta", "sexta"],
                    "timestamp_end": "18:59",
                    "timestamp_start": "00:00",
                    "utc_offset": -2,
                },
                {
                    "days": ["segunda", "terca", "quarta", "quinta", "domingo"],
                    "timestamp_end": "13:59",
                    "timestamp_start": "01:00",
                    "utc_offset": -3,
                },
            ],
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1y"), fake.time()),
        }

    @staticmethod
    def get_mock_profile_type_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        company_id: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()

        return {
            "id": id,
            "name": fake.word() if name is None else name,
            "profiles": ["INDOOR_PLANT", "OUTSIDE_PLANT", "CLIENT_HOUSE"],
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1y"), fake.time()),
        }

    @staticmethod
    def get_mock_log_time_series(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        owner_id: str = str(uuid.uuid4()),
        project: str = None,
    ) -> dict:
        fake = Faker()
        key = fake.word()
        value = 10
        return {
            "id": id,
            "value": value,
            "key": key,
            "owner_id": owner_id,
            "project": project,
            "company_id": company_id,
            "datetime_created": "{} {}".format(fake.date_between("-1d"), fake.time()),
        }

    @staticmethod
    def get_mock_component(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        template_id: str = str(uuid.uuid4()),
        description: str = None,
        devices: str = None,
    ) -> dict:
        fake: Faker = Faker()

        if description is None:
            description = fake.word()

        neighborhood = fake.word()
        city = fake.word()
        state = fake.word()
        street = fake.word()

        info = fake.text()
        fake.word()
        datetime_created = "{} {}".format(fake.date_between("-1d"), fake.time())

        return {
            "id": id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "company_id": company_id,
            "accepted": False,
            "latitude": -3.731862,
            "longitude": -38.526669,
            "description": description,
            "devices": [devices] if devices else [],
            "template_data": [
                {"field_name": "Zona", "field_type": "string", "field_value": "1"}
            ],
            "template_id": template_id,
            "info": info,
            "project": project,
            "neighborhood": neighborhood,
            "city": city,
            "state": state,
            "serial_number": "",
            "street": street,
            "datetime_created": datetime_created,
            "datetime_updated": datetime_created,
            "osp_id": None,
            "osp_project_id": None,
            "deactivated": False,
        }

    @staticmethod
    def get_mock_component_batch(
        id: str = str(uuid.uuid4()),
        template_id: str = str(uuid.uuid4()),
        description: str = None,
        device: str = None,
    ) -> dict:
        fake: Faker = Faker()

        if description is None:
            description = fake.word()

        neighborhood = fake.word()
        city = fake.word()
        state = fake.word()
        street = fake.word()

        info = fake.text()
        fake.word()
        datetime_created = "{} {}".format(fake.date_between("-1d"), fake.time())

        return {
            "id": id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "accepted": False,
            "latitude": -3.731862,
            "longitude": -38.526669,
            "description": description,
            "device": device,
            "template_data": [
                {"field_name": "Zona", "field_type": "string", "field_value": "1"}
            ],
            "template_id": template_id,
            "info": info,
            "neighborhood": neighborhood,
            "city": city,
            "state": state,
            "serial_number": "",
            "street": street,
            "datetime_created": datetime_created,
            "datetime_updated": datetime_created,
            "osp_id": None,
            "osp_project_id": None,
        }

    @staticmethod
    def get_mock_device(
        id: str = str(uuid.uuid4()),
        sort_key: str = None,
        description: str = None,
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        status: str = "ACTIVE",
        identificator_in_network: str = str(uuid.uuid4()),
        model_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        protocol: str = "LoRaWAN TTI",
    ):
        if sort_key is None:
            sort_key = f"devices#{company_id}#{project}"

        fake = Faker()
        if description is None:
            description = fake.word()

        return {
            "id": id,
            "project": project,
            "company_id": company_id,
            "identificator_in_network": identificator_in_network,
            "model_id": model_id,
            "supressed": False,
            "description": description,
            "info": fake.text(),
            "status": status,
            "updated_by": created_by,
            "created_by": created_by,
            "datetime_created": "{} {}".format(fake.date_between("-1d"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1d"), fake.time()),
            "datetime_last_alarm": "{} {}".format(
                fake.date_between("-1d"), fake.time()
            ),
            "datetime_last_contact": "{} {}".format(
                fake.date_between("-1d"), fake.time()
            ),
            "serial_number": "00310",
            "timer": "3h",
        }

    @staticmethod
    def get_mock_template_data(
        id: str = str(uuid.uuid4()),
        template_name: str = None,
        fields: list = [],
        company_id: str = str(uuid.uuid4()),
        has_acceptance: bool = True,
        has_maintenance: bool = True,
        osp_integration_compliant: bool = False,
        template_data: dict = {},
        type="ACCESSORY",
    ) -> dict:
        fake: Faker = Faker()
        return {
            "id": id,
            "name": template_name if template_name is not None else fake.word(),
            "fields": fields,
            "icon_code": fake.word().upper(),
            "has_acceptance": has_acceptance,
            "has_maintenance": has_maintenance,
            "external_client_visible_oem": False,
            "external_client_visible_acceptance": False,
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "osp_integration_compliant": osp_integration_compliant,
            "template_data": template_data,
            "type": type,
        }

    @staticmethod
    def get_mobile_users_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        team_id: str = str(uuid.uuid4()),
        name: str = None,
        family_name: str = None,
        email: str = None,
        phone_number: str = None,
        language: Literal["pt-BR", "en-US", "es-ES"] = "pt-BR",
    ) -> dict:
        fake: Faker = Faker()

        if name is None:
            name = fake.name()
        if family_name is None:
            family_name = fake.last_name()
        if email is None:
            email = fake.email()
        if phone_number is None:
            phone_number = "+" + str(fake.random_number(13))
        if language is None:
            language = "pt-BR"

        return {
            "id": id,
            "name": name,
            "family_name": family_name,
            "email": email,
            "phone_number": phone_number,
            "language": language,
            "status": "CONFIRMED",
            "enabled": True,
            "available": True,
            "profile_types": ["TEST"],
            "team_id": team_id,
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_location": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "image_path": f"{company_id}/technicians/{id}.png",
            "push_mobile_token": None,
            "accredited_id": None,
        }

    @staticmethod
    def get_webhook_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        name: str = None,
        event: str = None,
        body_type: str = "CUSTOM",
    ) -> dict:
        fake: Faker = Faker()

        if name is None:
            name = fake.name()

        url = fake.url()
        if event is None:
            event = fake.word()
        headers = {"Content-Type": "application/json"}
        datetime_created = "{} {}".format(fake.date_between("-1d"), fake.time())
        body_fields = {}
        if body_type == "CUSTOM":
            body_fields = {
                "id": "id",
                "status": "status",
                "name": "name",
                "unit": "unit",
                "qtd_min": "qtd_min",
                "company_id": "company_id",
            }

        return {
            "id": id,
            "name": name,
            "url": url,
            "event": event,
            "headers": headers,
            "body_fields": body_fields,
            "enabled": True,
            "body_type": body_type,
            "company_id": company_id,
            "created_by": "SYSTEM",
            "updated_by": "SYSTEM",
            "datetime_created": datetime_created,
            "datetime_updated": datetime_created,
        }

    @staticmethod
    def get_mock_attendance_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        type_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        customer: str = None,
        project: str = str(uuid.uuid4()),
        latitude: float = None,
        longitude: float = None,
        technician_id: str = str(uuid.uuid4()),
        technician_name: str = None,
        technician_email: str = None,
        status: str = "OPEN",
        tasks: list = [str(uuid.uuid4())],
        associated_technicians_ids: list = [str(uuid.uuid4())],
        protocols: list = [str(uuid.uuid4())],
        datetime_created: datetime = datetime.now() - timedelta(hours=3),
        component_id: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()

        datetime_start = "{} {}".format(fake.date_between("-1y"), fake.time())
        datetime_end = "{} {}".format(fake.date_between("-1y"), fake.time())

        if datetime_created is not None:
            datetime_start = datetime_created.strftime("%Y-%m-%d %H:%M:%S")

        if latitude is None:
            latitude = float(fake.latitude())
        if longitude is None:
            longitude = float(fake.longitude())
        if technician_id is None and status != "OPEN":
            technician_id = str(uuid.uuid4())
        if technician_name is None and status != "OPEN":
            technician_name = fake.name()
        if technician_email is None and status != "OPEN":
            technician_email = fake.email()

        if technician_id is not None and associated_technicians_ids is not None:
            associated_technicians_ids.append(technician_id)

        if customer is None:
            customer = fake.name()

        return {
            "id": id,
            "code": datetime_created.strftime("%Y%m%d%H%M%S%d"),
            "type_id": type_id,
            "created_by": created_by,
            "updated_by": created_by,
            "status": status,
            "project": project,
            "latitude": latitude,
            "longitude": longitude,
            "reason": fake.text(),
            "address": fake.address(),
            "customer": customer,
            "company_id": company_id,
            "priority": 5,
            "technician_id": technician_id,
            "technician_name": technician_name,
            "technician_email": technician_email,
            "tasks": tasks,
            "associated_technicians_ids": associated_technicians_ids,
            "protocols": protocols,
            "datetime_expected_start": datetime_start,
            "datetime_expected_end": datetime_end,
            "datetime_read": None,
            "datetime_confirmed": None,
            "datetime_departured": None,
            "datetime_arrived": None,
            "datetime_started": None,
            "datetime_finished": None,
            "datetime_approved": None,
            "datetime_created": datetime_start,
            "datetime_updated": datetime_start,
            "estimated_access": 10,
            "estimated_coil_size": 40,
            "estimated_consumption": 35,
            "estimated_left": 5,
            "estimated_measure": 10,
            "component_id": component_id,
        }

    @staticmethod
    def mock_user_simplified_data(
        company_id: str,
    ) -> dict:
        fake = Faker()
        user_data = {
            "id": str(uuid.uuid4()),
            "sort_key": "users#" + str(uuid.uuid4()),
            "company_id": company_id,
            "searchable_family_name": fake.name(),
            "function_tag": [],
            "projects": [str(uuid.uuid4()), str(uuid.uuid4())],
            "status": "CONFIRMED",
            "hierarchy": fake.word(),
            "family_name": fake.name(),
            "email": fake.email(),
            "name": fake.name(),
            "telegram_id": fake.word(),
            "enabled": 1,
            "searchable_name": fake.name(),
            "push_mobile_token": None,
            "push_web_token": "cXusPS_A57m1Ym8LWh2pyr:APA91bHtDaUJXeVj8lrSGs1VWagywHDv79l2YCp869KF1rIkpKqal45vfdHrVxYK-TMAbkCdAL2pH-qbJMq9lZ2YeoCvhu4TJoNkBbdnBDLpPr8rsIyBzbZd0eQFgiZAB-xjll6Vj8WC",
            "phone_number": fake.phone_number(),
            "permission": str(uuid.uuid4()),
            "sortable_field": fake.name() + str(uuid.uuid4()),
            "imagem_path": str(uuid.uuid4()),
        }
        return {
            "id": str(uuid.uuid4()),
            "name": fake.name(),
            "email": fake.email(),
            "user_data": user_data,
            "company_id": company_id,
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "datetime_created": f"{fake.date()} {fake.time()}",
            "datetime_updated": f"{fake.date()} {fake.time()}",
        }

    @staticmethod
    def get_mock_device_downlink(
        id: str = str(uuid.uuid4()),
        device_id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        f_port: str = "5",
        payload: str = "2d",
        datetime_created: datetime = datetime.now() - timedelta(hours=3),
        created_by: str = str(uuid.uuid4()),
    ):
        return {
            "id": f"{str(datetime_created.timestamp()).split(sep='.')[0]}_{id}",
            "sort_key": f"device_downlinks#{company_id}",
            "device_id": device_id,
            "company_id": company_id,
            "payload": payload,
            "fport": f_port,
            "created_by": created_by,
            "datetime_created": Decimal(datetime_created.timestamp()),
            "secondary_sort_key": f"device_downlinks#device_id#{device_id}",
        }

    @staticmethod
    def get_mock_device_dynamodb(
        id: str = str(uuid.uuid4()),
        sort_key: str = None,
        description: str = None,
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        status: str = "ACTIVE",
        identificator_in_network: str = str(uuid.uuid4()),
        model_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        protocol: str = "LoRaWAN TTI",
        datetime_created: datetime = None,
        lat: Optional[str] = None,
        long: Optional[str] = None,
        reasons: List[str] = None,
    ):
        if sort_key is None:
            sort_key = f"devices#{company_id}#{project}"

        fake = Faker()
        if description is None:
            description = fake.word()

        if datetime_created is None:
            datetime_str = "{} {}".format(fake.date_between("-1y"), fake.time())
            datetime_created = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        datetime_str = "{} {}".format(fake.date_between("-1y"), fake.time())
        datetime_last_alarm = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        datetime_str = "{} {}".format(fake.date_between("-1y"), fake.time())
        datetime_last_contact = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        if lat is None:
            lat = str(fake.coordinate())
        if long is None:
            long = str(fake.coordinate())

        return {
            "id": id,
            "sort_key": sort_key,
            "project": project,
            "company_id": company_id,
            "identificator_in_network": identificator_in_network,
            "model_id": model_id,
            "supressed": False,
            "description": description,
            "sortable_field": f"{description} {id}",
            "info": fake.text(),
            "status": status,
            "secondary_sort_key": f"devices#{protocol}#{identificator_in_network}",
            "updated_by": created_by,
            "created_by": created_by,
            "datetime_created": Decimal(datetime_created.timestamp()),
            "datetime_updated": Decimal(datetime_created.timestamp()),
            "datetime_last_alarm": Decimal(datetime_last_alarm.timestamp()),
            "datetime_last_contact": Decimal(datetime_last_contact.timestamp()),
            "model_fields": {"device_eui": identificator_in_network},
            "network_server": "TTI",
            "searchable_description": description,
            "serial_number": "00310",
            "lat": lat,
            "long": long,
            "reasons": reasons,
            "last_reasons": None,
            "last_status": None,
        }

    @staticmethod
    def get_mock_device_latest_dynamodb(
        id: str = str(uuid.uuid4()),
        sort_key: str = None,
        description: str = None,
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        status: str = "ACTIVE",
        identificator_in_network: str = str(uuid.uuid4()),
    ):
        if sort_key is None:
            sort_key = f"devices_latest#{company_id}#{project}"

        fake = Faker()
        if description is None:
            description = fake.word()

        return {
            "id": id,
            "sort_key": sort_key,
            "project": project,
            "company_id": company_id,
            "identificator_in_network": identificator_in_network,
            "description": description,
            "sortable_field": f"{description} {id}",
            "status": status,
            "searchable_description": description,
        }

    @staticmethod
    def get_mock_device_log(
        id: str = None,
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        device_id: str = str(uuid.uuid4()),
        description: str = None,
        identificator_in_network: str = str(uuid.uuid4()),
        status: str = "ALARMED",
        actived_by_user_id: str = str(uuid.uuid4()),
        datetime_created: datetime = datetime.now() - timedelta(hours=3),
        causes: list = ["luminosity", "moviment"],
    ):
        fake = Faker()
        if description is None:
            description = fake.word()
        if id is None:
            id = str(datetime_created.timestamp()) + "-" + str(uuid.uuid4())

        return {
            "actived_by_user_id": actived_by_user_id,
            "company_id": company_id,
            "datetime_created": Decimal(datetime_created.timestamp()),
            "description": description,
            "id": id,
            "device_id": device_id,
            "last_alarm_causes": causes,
            "rssi": Decimal(str(fake.pyfloat())),
            "snr": Decimal(str(fake.pyfloat())),
            "temperature": Decimal(str(fake.pyfloat())),
            "frequencia": str(fake.pyint()),
            "gateway_id": str(uuid.uuid4()),
            "luminosity": Decimal(str(fake.pyfloat())),
            "manutencoes": [],
            "acelerometer_x": Decimal(str(fake.pyfloat())),
            "acelerometer_y": Decimal(str(fake.pyfloat())),
            "acelerometer_z": Decimal(str(fake.pyfloat())),
            "acelerometer_roll": None,
            "acelerometer_pitch": None,
            "power_meter": None,
            "battery": Decimal(str(fake.pyfloat())),
            "canal": Decimal(fake.pyint()),
            "counter": Decimal(fake.pyint()),
            "fport": Decimal(fake.pyint()),
            "payload": "{}",
            "identificator_in_network": identificator_in_network,
            "status": status,
            "project": project,
            "sort_key": f"log_devices#{company_id}#{device_id}",
        }

    @staticmethod
    def get_mock_device_status_change_log(
        id: str = None,
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        description: str = None,
        identificator_in_network: str = str(uuid.uuid4()),
        original_status: str = "---",
        new_status: str = "PENDING",
        actived_by_user_id: str = str(uuid.uuid4()),
        datetime_created: datetime = datetime.now() - timedelta(hours=3),
        causes: list = ["moviment"],
    ):
        fake = Faker()
        if description is None:
            description = fake.word()
        if id is None:
            id = datetime_created.timestamp() + "-" + str(uuid.uuid4())

        return {
            "actived_by_user_id": actived_by_user_id,
            "company_id": company_id,
            "datetime_created": Decimal(datetime_created.timestamp()),
            "description": description,
            "id": id,
            "causes": causes,
            "identificator_in_network": identificator_in_network,
            "new_status": new_status,
            "original_status": original_status,
            "project": project,
            "sort_key": f"log_devices_variance#{company_id}#{project}",
        }

    @staticmethod
    def get_mock_device_notification(
        id: str = str(uuid.uuid4()),
        name: Union[str, None] = None,
        module: str = "Iot",
        all_devices: bool = False,
        devices: list = [],
        channels: dict = {},
        project: str = str(uuid.uuid4()),
        users: list = [],
        active: bool = True,
        company_id: str = str(uuid.uuid4()),
        created_by: str = str(uuid.uuid4()),
        datetime_created: datetime = datetime.now() + timedelta(hours=-3),
    ):
        fake = Faker()
        if name is None:
            name = fake.word()

        return {
            "id": id,
            "sort_key": f"device_notifications#{company_id}#{project}",
            "sortable_field": f"{name} {id}",
            "name": name,
            "module": module,
            "all_devices": all_devices,
            "devices": devices,
            "channels": channels,
            "project": project,
            "users": users,
            "active": active,
            "company_id": company_id,
            "created_by": created_by,
            "updated_by": created_by,
            "datetime_created": int(datetime_created.timestamp()),
            "datetime_updated": int(datetime_created.timestamp()),
        }

    @staticmethod
    def get_mock_attendance_report_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        status: str = "RECEIVED",
        attendance_id: str = str(uuid.uuid4()),
        technician_id: str = str(uuid.uuid4()),
        technician_name: str = None,
        technician_email: str = None,
        latitude: float = None,
        longitude: float = None,
        questions_status: str = "ANSWERED",
        not_evaluation_reason: str = None,
        signature_image: str = None,
        customer: str = None,
        tasks_report: dict = {
            "text": "",
            "after": [],
            "before": [],
            "additional": [],
            "issue_status": "SOLVED",
        },
        refused_tasks: list = [],
        onu_task_report: dict = {
            "onu_task_id": str(uuid.uuid4()),
            "fields": {"field": "name", "value": "Julius"},
        },
        questions_report: list = [],
        datetime_created: datetime = datetime.now() - timedelta(hours=3),
        created_by: str = str(uuid.uuid4()),
        indicators: list = [str(uuid.uuid4())],
        drop_subscriber: dict = {
            "coil_size": 53,
            "consumption": 11,
            "has_drop_subscriber": True,
            "justification": "some justification",
            "left_footage": 1,
            "serial_number": "TC166",
        },
        items: list = [
            {
                "serial_number": "TC001",
                "item": {"id": "3", "consumed": 2},
                "status": "NEW",
            },
            {
                "serial_number": None,
                "item": {"id": "1", "consumed": 8},
                "status": "NEW",
            },
        ],
    ) -> dict:
        fake: Faker = Faker()
        datetime_str = "{} {}".format(fake.date_between("-1y"), fake.time())
        if datetime_created is not None:
            datetime_str = datetime_created.strftime("%Y-%m-%d %H:%M:%S")

        if customer is None:
            customer = fake.name()
        if technician_name is None:
            technician_name = fake.name()
        if technician_email is None:
            technician_email = fake.email()

        if latitude is None:
            latitude = fake.pyfloat()
        if longitude is None:
            longitude = fake.pyfloat()

        return {
            "id": id,
            "created_by": created_by,
            "updated_by": created_by,
            "status": status,
            "project": project,
            "company_id": company_id,
            "attendance_id": attendance_id,
            "technician_id": technician_id,
            "technician_name": technician_name,
            "technician_email": technician_email,
            "latitude": latitude,
            "longitude": longitude,
            "time_lapse": fake.pyfloat(),
            "questions_status": questions_status,
            "not_evaluation_reason": not_evaluation_reason,
            "signature_image": signature_image,
            "customer": customer,
            "tasks_report": tasks_report,
            "refused_tasks": refused_tasks,
            "questions_report": questions_report,
            "datetime_received": datetime_str,
            "datetime_expected_start": datetime_str,
            "datetime_expected_end": datetime_str,
            "datetime_start": datetime_str,
            "datetime_end": datetime_str,
            "datetime_created": datetime_str,
            "datetime_updated": datetime_str,
            "onu_task_report": onu_task_report,
            "items": items,
            "indicators": indicators,
            "drop_subscriber": drop_subscriber,
        }

    @staticmethod
    def get_mock_acceptance_report_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
    ) -> dict:
        return {"id": id, "project": project, "company_id": company_id}

    @staticmethod
    def get_mock_maintenance_report_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        indicators: List[str] = [],
        maintenance_id: str = str(uuid.uuid4()),
        technician_id: str = str(uuid.uuid4()),
        status: str = "ACCEPTED",
        datetime_received: datetime = datetime.now() + timedelta(hours=-3),
    ) -> dict:
        return {
            "id": id,
            "project": project,
            "company_id": company_id,
            "indicators": indicators,
            "maintenance_id": maintenance_id,
            "technician_id": technician_id,
            "status": status,
            "datetime_received": datetime_received,
        }

    def get_mock_deployment_plan_data(
        id: str = str(uuid.uuid4()),
        name: str = None,
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.word()

        return {
            "id": id,
            "name": name,
            "company_id": company_id,
            "project": project,
        }

    @staticmethod
    def get_client_house_protocol_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
        code: str = str(uuid.uuid4()),
        protocol_code: str = str(uuid.uuid4()),
    ) -> dict:
        return {
            "id": id,
            "project": project,
            "company_id": company_id,
            "code": code,
            "protocol_code": protocol_code,
        }

    @staticmethod
    def get_mock_devices_dashboard(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
    ):
        return {
            "id": id,
            "company_id": company_id,
            "project": project,
        }

    @staticmethod
    def get_material_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
    ) -> dict:
        return {"id": id, "project": project, "company_id": company_id}

    @staticmethod
    def get_technician_transfer_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
    ) -> dict:
        return {"id": id, "project": project, "company_id": company_id}

    @staticmethod
    def get_main_transfer_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project: str = str(uuid.uuid4()),
    ) -> dict:
        return {"id": id, "project": project, "company_id": company_id}

    @staticmethod
    def get_mock_maintenance_indicator_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        name: str = None,
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.word()

        return {
            "id": id,
            "company_id": company_id,
            "name": name,
        }

    @staticmethod
    def mock_audit_user_record(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        entity_type: str = "users",
        datetime_start=datetime.now(),
        method: Optional[str] = None,
        new_data: Optional[dict] = None,
        old_data: Optional[dict] = None,
        entity_id: Optional[str] = None,
        project: Optional[str] = None,
    ) -> dict:
        fake = Faker()
        module = fake.word()
        identificator_key = "name"
        identificator_value = fake.name()
        user_id = fake.word()
        user_name = fake.name() + " " + fake.last_name()
        user_email = fake.email()
        if not old_data:
            old_data = {"id": identificator_value, "value": "old"}
        new_data_to_use = (
            {"id": identificator_value, "value": "new"}
            if new_data is None
            else new_data
        )
        return {
            "id": id,
            "entity_type": entity_type,
            "project": project,
            "entity_id": entity_id,
            "module": module,
            "method": method,
            "identificator_key": identificator_key,
            "identificator_value": identificator_value,
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "old_data": old_data,
            "new_data": new_data_to_use,
            "datetime_log": f"{datetime_start}",
            "company_id": company_id,
        }

    @staticmethod
    def build_insert_sql(table_name: str, entity: dict) -> str:
        columns = []
        values = []
        for key in entity:
            columns.append(key)
            if isinstance(entity[key], dict) or isinstance(entity[key], list):
                values.append("'" + json.dumps(entity[key]) + "'")
            elif isinstance(entity[key], str):
                values.append("'" + entity[key] + "'")
            elif isinstance(entity[key], int) or isinstance(entity[key], float):
                values.append(str(entity[key]))
            elif isinstance(entity[key], bool):
                values.append(str(entity[key]).lower())
            elif isinstance(entity[key], datetime):
                values.append("'" + entity[key].strftime("%Y-%m-%d %H:%M:%S") + "'")
            elif entity[key] is None:
                values.append("NULL")
            else:
                values.append(entity[key])
        columns_string = ",".join(columns)
        values_string = ",".join(values)
        return """INSERT INTO {} ({}) VALUES ({});""".format(
            table_name, columns_string, values_string
        )

    @staticmethod
    def get_mock_admin_direct_email(
        id: str = str(uuid.uuid4()),
        report_type: str = "detailed_report",
        name: Union[str, None] = None,
        email: Union[str, None] = None,
        datetime_updated: Union[datetime, None] = None,
        datetime_created: Union[datetime, None] = datetime.utcnow()
        + timedelta(hours=-3),
        companies: List[str] = [],
        company_id: str = "SYS_FURUKAWA",
        created_by: str = "SYSTEM",
        updated_by: str = "SYSTEM",
    ) -> dict:
        fake: Faker = Faker()
        if name is None:
            name = fake.word()
        if email is None:
            email = fake.email()

        return {
            "id": id,
            "report_type": report_type,
            "name": name,
            "email": email,
            "datetime_updated": datetime_updated,
            "datetime_created": datetime_created,
            "companies": companies,
            "company_id": company_id,
            "created_by": created_by,
            "updated_by": updated_by,
        }

    @staticmethod
    def get_technician_stock_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project_id: str = str(uuid.uuid4()),
        owner_id: str = str(uuid.uuid4()),
    ) -> dict:
        return {
            "id": id,
            "owner_id": owner_id,
            "project": project_id,
            "company_id": company_id,
        }

    @staticmethod
    def get_individual_material_data(
        id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        project_id: str = str(uuid.uuid4()),
        owner_id: str = str(uuid.uuid4()),
        qtd: int = 10,
    ) -> dict:
        return {
            "id": id,
            "owner_id": owner_id,
            "project": project_id,
            "company_id": company_id,
            "qtd": qtd,
        }

    @staticmethod
    def get_mock_sql_company_data(
        id: str = str(uuid.uuid4()),
        name: str = Faker().name(),
        status: str = "ACTIVE",
    ) -> dict:
        fake: Faker = Faker()

        return {
            "id": id,
            "name": name,
            "email": fake.email(),
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "datetime_updated": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "created_by": str(uuid.uuid4()),
            "updated_by": str(uuid.uuid4()),
            "status": status,
        }

    @staticmethod
    def get_mock_os_registration_data(
        id: str = str(uuid.uuid4()),
        os_id: str = str(uuid.uuid4()),
        company_id: str = str(uuid.uuid4()),
        os_type: str = "MAINTENANCE",
        project: str = str(uuid.uuid4()),
    ) -> dict:
        fake: Faker = Faker()

        return {
            "id": id,
            "os_id": os_id,
            "company_id": company_id,
            "os_type": os_type,
            "project": project,
            "datetime_created": "{} {}".format(fake.date_between("-1y"), fake.time()),
            "created_by": str(uuid.uuid4()),
            "created_by_name": fake.name(),
        }
