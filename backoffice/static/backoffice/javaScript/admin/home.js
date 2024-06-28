$(document).ready(function(){
    // Carregar modal de criação
    $('.add').on('click', function(event) {
        event.preventDefault(); // Impede a navegação padrão
        $.ajax({
            url: '{% url "user_create" %}',
            type: 'GET',
            success: function(data) {
                $('#modalContainer').html(data);
                $('#addEmployeeModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Erro ao carregar o modal de criação:', status, error);
            }
        });
    });

    // Intercepta cliques em botões de edição
    $(document).on('click', '.edit', function(event) {
        event.preventDefault(); // Impede a navegação padrão
        var userId = $(this).data('id');
        $.ajax({
            url: '/users/' + userId + '/edit/',
            type: 'GET',
            success: function(data) {
                $('#modalContainer').html(data);
                $('#editEmployeeModal').modal('show');
            },
            error: function(xhr, status, error) {
                console.error('Erro ao carregar o modal de edição:', status, error);
            }
        });
    });

    // Intercepta cliques em botões de deleção
    $(document).on('click', '.delete', function(event) {
        event.preventDefault(); // Impede a navegação padrão
        var userId = $(this).data('id');
        $.ajax({
            url: '/users/' + userId + '/delete/',
            type: 'GET',
            success: function(data) {
                $('#modalContainer').html(data);
                $('#deleteEmployeeModal').modal('show');
                // Adiciona a funcionalidade de deleção
                $('#deleteForm').on('submit', function(event) {
                    event.preventDefault();
                    $.ajax({
                        url: '/users/' + userId + '/delete/',
                        type: 'POST',
                        data: $(this).serialize(),
                        success: function(data) {
                            $('#deleteEmployeeModal').modal('hide');
                            location.reload(); // Recarrega a página para refletir as mudanças
                        },
                        error: function(xhr, status, error) {
                            console.error('Erro ao apagar o usuário:', status, error);
                        }
                    });
                });
            },
            error: function(xhr, status, error) {
                console.error('Erro ao carregar o modal de deleção:', status, error);
            }
        });
    });

    // Carregar e exibir usuários na tabela
    function loadUsers() {
        $.ajax({
            url: '/api/users/',  // URL corrigida
            type: 'GET',
            success: function(data) {
                let usersList = $('#users-list');
                usersList.empty();
                data.forEach(user => {
                    let row = `
                        <tr>
                            <td>
                                <span class="custom-checkbox">
                                    <input type="checkbox" id="checkbox${user.id}" name="options[]" value="${user.id}">
                                    <label for="checkbox${user.id}"></label>
                                </span>
                            </td>
                            <td>${user.username}</td>
                            <td>${user.email}</td>
                            <td>
                                <input type="password" value="${user.password}" class="form-control password-field" readonly>
                                <button class="btn btn-link toggle-password" data-password="${user.password}">Mostrar</button>
                            </td>
                            <td>${user.date_joined}</td>
                            <td>${user.created_by}</td>
                            <td>${user.last_modified}</td>
                            <td>${user.modified_by}</td>
                            <td>
                                <a href="#" class="edit" data-id="${user.id}" data-toggle="modal" data-target="#editEmployeeModal"><i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i></a>
                                <a href="#" class="delete" data-id="${user.id}" data-toggle="modal" data-target="#deleteEmployeeModal"><i class="material-icons" data-toggle="tooltip" title="Delete">&#xE872;"></i></a>
                            </td>
                        </tr>`;
                    usersList.append(row);
                });

                // Adiciona event listeners para os botões de mostrar senha
                $('.toggle-password').on('click', function() {
                    let passwordField = $(this).prev('.password-field');
                    if (passwordField.attr('type') === 'password') {
                        passwordField.attr('type', 'text');
                        $(this).text('Ocultar');
                    } else {
                        passwordField.attr('type', 'password');
                        $(this).text('Mostrar');
                    }
                });
            },
            error: function(xhr, status, error) {
                console.error('Erro ao carregar a lista de usuários:', status, error);
            }
        });
    }

    // Carrega os usuários ao carregar a página
    loadUsers();
});
