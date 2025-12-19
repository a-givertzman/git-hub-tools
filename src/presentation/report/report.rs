use iced::{Element, Task, Theme, widget::button};

#[derive(Debug, Clone)]
pub enum Message {
    FetchReport,
    ReportFetched(Commits),
}
#[derive(Debug, Clone)]
pub struct Commits {}
pub struct Report {}
impl Report {
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
