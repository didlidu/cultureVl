CKEDITOR.plugins.add( 'author', 
{
	init: function( editor )
	{
		editor.addCommand( 'insertAuthor',
		{
			exec : function( editor )
			{    
				var selection = editor.getSelection();
				editor.insertHtml( '<a href="/author/' + selection.getSelectedText() + '">' + selection.getSelectedText() + '</a>'  );
			}
		});
		editor.ui.addButton( 'author',
		{
			label: 'Вставка Автора',
			command: 'insertAuthor',
			icon: this.path + 'author.png'
		} );
	}
} );

