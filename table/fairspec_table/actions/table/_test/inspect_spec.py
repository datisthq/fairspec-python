from __future__ import annotations

import polars as pl
from fairspec_metadata import NumberColumnProperty
from fairspec_metadata import StringColumnProperty
from fairspec_metadata import ColumnMissingError
from fairspec_metadata import TableSchema

from ..inspect import inspect_table


class TestInspectTable:
    def test_should_pass_when_columns_exactly_match(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
                "name": ["John", "Jane"],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_not_have_columns_error_when_columns_same_length(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
                "age": [30, 25],
            }
        ).lazy()

        table_schema = TableSchema(
            allRequired=True,
            properties={
                "id": NumberColumnProperty(),
                "name": NumberColumnProperty(),
            },
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert len(errors) == 1
        assert isinstance(errors[0], ColumnMissingError)
        assert errors[0].columnName == "name"

    def test_should_detect_missing_columns(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            allRequired=True,
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            },
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert len(errors) == 1
        assert isinstance(errors[0], ColumnMissingError)
        assert errors[0].columnName == "name"

    def test_should_pass_when_column_names_match_regardless_of_order(self):
        table = pl.DataFrame(
            {
                "name": ["John", "Jane"],
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_detect_missing_columns_with_required(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            required=["name"],
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            },
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert len(errors) == 1
        assert isinstance(errors[0], ColumnMissingError)
        assert errors[0].columnName == "name"

    def test_should_pass_when_non_required_columns_are_missing(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_pass_when_data_contains_all_schema_columns(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
                "name": ["John", "Jane"],
                "age": [30, 25],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_pass_when_data_contains_exact_schema_columns(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
                "name": ["John", "Jane"],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_detect_missing_columns_again(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            required=["name"],
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            },
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert len(errors) == 1
        assert isinstance(errors[0], ColumnMissingError)
        assert errors[0].columnName == "name"

    def test_should_pass_when_schema_contains_all_data_columns(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_pass_when_schema_contains_exact_data_columns(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
                "name": ["John", "Jane"],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_pass_when_at_least_one_column_matches(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
                "age": [30, 25],
            }
        ).lazy()

        table_schema = TableSchema(
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            }
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert errors == []

    def test_should_detect_missing_columns_with_all_required(self):
        table = pl.DataFrame(
            {
                "id": [1, 2],
            }
        ).lazy()

        table_schema = TableSchema(
            allRequired=True,
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            },
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert len(errors) == 1
        assert isinstance(errors[0], ColumnMissingError)
        assert errors[0].columnName == "name"

    def test_should_detect_when_no_columns_match(self):
        table = pl.DataFrame(
            {
                "age": [30, 25],
                "email": ["john@example.com", "jane@example.com"],
            }
        ).lazy()

        table_schema = TableSchema(
            allRequired=True,
            properties={
                "id": NumberColumnProperty(),
                "name": StringColumnProperty(),
            },
        )

        errors = inspect_table(table, table_schema=table_schema)

        assert len(errors) == 2
        assert isinstance(errors[0], ColumnMissingError)
        assert errors[0].columnName == "id"
        assert isinstance(errors[1], ColumnMissingError)
        assert errors[1].columnName == "name"
