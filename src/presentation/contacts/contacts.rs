use iced::{Element, Length::Fill, Theme, widget::{button, column, container, row}};
use super::{Action, Message};

#[derive(Debug, Clone)]
pub struct Contacts {}
impl Contacts {
    pub fn update(&self, message: Message) -> Action {
        Action::None
    }
    pub fn view(&self) -> Element<'_, Message> {
        container(
            column![
                "Contacts",
                button("I am a styled button!").style(|theme: &Theme, status| {
                    let palette = theme.extended_palette();
                    match status {
                        button::Status::Active => {
                            button::Style::default()
                               .with_background(palette.success.strong.color)
                        }
                        _ => button::primary(theme, status),
                    }
                }).on_press(Message {}),
                row!["Left", "Right"].spacing(10),
                "Bottom"
            ]
            .spacing(10)
        )
        .padding(10)
        .center_x(Fill)
        .center_y(Fill)
        .into()
    
        // .into()
    }
}
