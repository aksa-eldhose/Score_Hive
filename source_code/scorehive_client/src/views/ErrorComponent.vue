<template>
  <div>
    <Table :columns="tableColumns" :rows="tableRows" aria-label="">
      <!-- Custom column -->
      <template v-slot:custom-columns>
        <th class="text-center">Actions</th>
      </template>

      <!-- Custom row -->
      <template v-slot:custom-rows="{ row, index }">
        <td class="text-center">
          <!-- Settings icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
            class="text-info cursor-pointer mx-1" style="width: 20px;">
            <path fill-rule="evenodd"
              d="M11.078 2.25c-.917 0-1.699.663-1.85 1.567L9.05 4.889c-.02.12-.115.26-.297.348a7.493 7.493 0 00-.986.57c-.166.115-.334.126-.45.083L6.3 5.508a1.875 1.875 0 00-2.282.819l-.922 1.597a1.875 1.875 0 00.432 2.385l.84.692c.095.078.17.229.154.43a7.598 7.598 0 000 1.139c.015.2-.059.352-.153.43l-.841.692a1.875 1.875 0 00-.432 2.385l.922 1.597a1.875 1.875 0 002.282.818l1.019-.382c.115-.043.283-.031.45.082.312.214.641.405.985.57.182.088.277.228.297.35l.178 1.071c.151.904.933 1.567 1.85 1.567h1.844c.916 0 1.699-.663 1.85-1.567l.178-1.072c.02-.12.114-.26.297-.349.344-.165.673-.356.985-.57.167-.114.335-.125.45-.082l1.02.382a1.875 1.875 0 002.28-.819l.923-1.597a1.875 1.875 0 00-.432-2.385l-.84-.692c-.095-.078-.17-.229-.154-.43a7.614 7.614 0 000-1.139c-.016-.2.059-.352.153-.43l.84-.692c.708-.582.891-1.59.433-2.385l-.922-1.597a1.875 1.875 0 00-2.282-.818l-1.02.382c-.114.043-.282.031-.449-.083a7.49 7.49 0 00-.985-.57c-.183-.087-.277-.227-.297-.348l-.179-1.072a1.875 1.875 0 00-1.85-1.567h-1.843zM12 15.75a3.75 3.75 0 100-7.5 3.75 3.75 0 000 7.5z"
              clip-rule="evenodd" />
          </svg>
          <!-- Edit icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
            class="text-warning cursor-pointer mx-1" style="width: 20px;">
            <path
              d="M21.731 2.269a2.625 2.625 0 00-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 000-3.712zM19.513 8.199l-3.712-3.712-8.4 8.4a5.25 5.25 0 00-1.32 2.214l-.8 2.685a.75.75 0 00.933.933l2.685-.8a5.25 5.25 0 002.214-1.32l8.4-8.4z" />
            <path
              d="M5.25 5.25a3 3 0 00-3 3v10.5a3 3 0 003 3h10.5a3 3 0 003-3V13.5a.75.75 0 00-1.5 0v5.25a1.5 1.5 0 01-1.5 1.5H5.25a1.5 1.5 0 01-1.5-1.5V8.25a1.5 1.5 0 011.5-1.5h5.25a.75.75 0 000-1.5H5.25z" />
          </svg>
          <!-- Delete icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
            class="text-danger cursor-pointer mx-1" style="width: 20px;">
            <path fill-rule="evenodd"
              d="M16.5 4.478v.227a48.816 48.816 0 013.878.512.75.75 0 11-.256 1.478l-.209-.035-1.005 13.07a3 3 0 01-2.991 2.77H8.084a3 3 0 01-2.991-2.77L4.087 6.66l-.209.035a.75.75 0 01-.256-1.478A48.567 48.567 0 017.5 4.705v-.227c0-1.564 1.213-2.9 2.816-2.951a52.662 52.662 0 013.369 0c1.603.051 2.815 1.387 2.815 2.951zm-6.136-1.452a51.196 51.196 0 013.273 0C14.39 3.05 15 3.684 15 4.478v.113a49.488 49.488 0 00-6 0v-.113c0-.794.609-1.428 1.364-1.452zm-.355 5.945a.75.75 0 10-1.5.058l.347 9a.75.75 0 101.499-.058l-.346-9zm5.48.058a.75.75 0 10-1.498-.058l-.347 9a.75.75 0 001.5.058l.345-9z"
              clip-rule="evenodd" />
          </svg>
        </td>
      </template>
    </Table>
    <h1 class="text-primary">Helloo</h1>
    <h1 class="text-secondary">Helloo</h1>
    <h1 class="text-danger">Helloo</h1>
    <h1 class="text-warning">Helloo</h1>
    <h1 class="text-dark">Helloo</h1>
    <h1 class="text-light">Helloo</h1>
    <button class="btn btn-primary ms-5">Submit</button>
    <button class="btn btn-secondary ms-5">Submit</button>
    <button class="btn btn-danger ms-5">Submit</button>
    <button class="btn btn-warning ms-5">Submit</button>
      <button class="btn btn-success ms-5">Submit</button>
    <button class="btn btn-dark ms-5">Submit</button>
    <button class="btn btn-light ms-5">Submit</button><br><br>
    <button class="btn btn-outline-primary ms-5">Submit</button>
    <button class="btn btn-outline-secondary ms-5">Submit</button>
    <button class="btn btn-outline-danger ms-5">Submit</button>
    <button class="btn btn-outline-warning ms-5">Submit</button>
    <button class="btn btn-outline-success ms-5">Submit</button>
    <button class="btn btn-outline-dark ms-5">Submit</button>
    <button class="btn btn-outline-light ms-5">Submit</button><br><br>
    <span class="bg-primary text-white p-2 ms-5">Span</span>
    <span class="bg-secondary p-2 ms-5">Span</span>
    <span class="bg-danger text-light p-2 ms-5">Span</span>
    <span class="bg-warning p-2 ms-5">Span</span>
    <span class="bg-success text-light p-2 ms-5">Span</span>
    <span class="bg-dark p-2 text-light ms-5">Span</span>
    <span class="bg-light p-2 ms-5">Span</span>
    <span class="bg-glass p-2 ms-5">Span</span><br><br>

  </div>
</template>

<script>
import Table from '@/components/TableComponent.vue';

export default {
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Table,
  },
  data() {
    return {
      tableColumns: ['Name', 'Age', 'Email', 'test'],
      tableRows: [
        { Name: 'John Doe', Age: 25, Email: 'johndoe@example.com' },
        { Name: 'Jane Smith', Age: 30, Email: 'janesmith@example.com' },
        { Name: 'Bob Johnson', Age: 35, Email: 'bobjohnson@example.com' },
      ],
    };
  },
};
</script>
