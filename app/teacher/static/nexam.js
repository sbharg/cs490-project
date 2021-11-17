$(function() {
    $('.q-link').dblclick(function(event) {
        event.preventDefault();
        var func_name = $(this).attr('q-link_name');
        var q_id = $(this).attr('q-link_id');
        var q_text = $(this).attr('q-link_text');
        var constraint = $(this).attr('q-link_constraint');
        var constraint_text = 'asdf'

        var func_cat = $(this).attr('q-link_cat');
        var func_diff = $(this).attr('q-link_diff');
        var diff_text = "Easy"

        switch (constraint){
            case 'for':
                constraint_text = "For Loop";
                break;
            case 'while':
                constraint_text = "While Loop";
                break;
            case 'rec':
                constraint_text = "Recursion";
                break;
            default:
                constraint_text = "None";
        }

        switch (func_diff){
            case 'easy':
                diff_text = "Easy";
                break;
            case 'medi':
                diff_text = "Medium";
                break;
            case 'hard':
                diff_text = "Hard";
                break;
        }

        $('#QuestionModal').find('#funcName').text(func_name);
        $('#QuestionModal').find('#funcConstraints').text(constraint_text);
        $('#QuestionModal').find('#funcCat').text(func_cat);
        $('#QuestionModal').find('#funcDiff').text(diff_text);
        $('#QuestionModal textarea').text(q_text);
        $('#QuestionModal').modal('show');
    });
  });
