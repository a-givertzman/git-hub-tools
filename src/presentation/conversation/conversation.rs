use iced::{Element, Task, Theme, widget::button};

use crate::contacts::Contact;

#[derive(Debug, Clone)]
pub struct Conversation {
    contact: Contact,
}
impl Conversation {
    pub fn new(contact: Contact) -> (Self, Task<Message>) {
        (
            Self {
                contact,
            },
            Task::none(),
        )
    }
    pub fn update(&self, message: Message) -> Task<Message> {
        Task::none()
    }
    pub fn view(&self) -> Element<'_, Message> {
        button("I am a styled button!").style(|theme: &Theme, status| {
            let palette = theme.extended_palette();
    
            match status {
                button::Status::Active => {
                    button::Style::default()
                       .with_background(palette.success.strong.color)
                }
                _ => button::primary(theme, status),
            }
        })
        .into()
    }
}
#[derive(Debug, Clone)]
pub struct Message {}
