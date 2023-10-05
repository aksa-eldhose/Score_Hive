<template>
    <table :class="getClass"  class="table table-hover text-center"
            style="border-collapse: collapse" aria-label="">
        <thead>
            <tr>
                <th id="" v-for="(column, index) in columns" :key="index">{{ column }}</th>
                <slot name="custom-columns"></slot>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
                <td v-for="(column, columnIndex) in columns" :key="columnIndex">
                    {{ row[column] }}
                </td>
                <slot name="custom-rows" :row="row" :index="rowIndex"></slot>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    props: {
        columns: {
            type: Array,
            required: true,
        },
        rows: {
            type: Array,
            required: true,
        },
        type: {
            type: String,
            default: '',
        },
    },
    computed: {
        getClass() {
            return this.type ? `table-${this.type}` : '';
        },
    },
};
</script>

<style scoped>
.table {
  width: 100%;
  border-collapse: collapse;
}
.table th,
.table td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.table th {
  background-color: #f2f2f2;
}

.table-striped tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table-bordered th,
.table-bordered td {
  border: 1px solid #ddd;
}

.table-hover tbody tr:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}

.fixed-size-table {
  table-layout: fixed;
}

.fixed-size-table th,
.fixed-size-table td {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Add additional styles as needed */

</style>

