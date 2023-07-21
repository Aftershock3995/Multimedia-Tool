using System;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using VideoLibrary;
using NAudio.Wave;

namespace Zipper
{
    public class Program : Form
    {
        private ComboBox cmbOptions;
        private TextBox txtFilePath;
        private Button btnExecute;
        private Label lblStatus;
        private ProgressBar progressBar;

        public Program()
        {
            InitializeComponents();
        }

        private void InitializeComponents()
        {
            this.Text = "Aftershocks Multimedia Tool";
            this.Size = new System.Drawing.Size(400, 240);
            this.StartPosition = FormStartPosition.CenterScreen;

            lblStatus = new Label();
            cmbOptions = new ComboBox();
            txtFilePath = new TextBox();
            btnExecute = new Button();
            progressBar = new ProgressBar();
 
            string backgroundColorHex = "#373737";
            string textColorHex = "#a9a9a9";
            string buttonColorHex = "#373737";
            string buttonBorderColorHex = "#f94c07";
            string progressBarColorHex = "#f94c07";  

            this.BackColor = HexToColor(backgroundColorHex);
            lblStatus.ForeColor = HexToColor(textColorHex);
            cmbOptions.BackColor = HexToColor(backgroundColorHex);
            cmbOptions.ForeColor = HexToColor(textColorHex);
            txtFilePath.BackColor = HexToColor(backgroundColorHex);
            txtFilePath.ForeColor = HexToColor(textColorHex);
            btnExecute.BackColor = HexToColor(buttonColorHex);
            btnExecute.ForeColor = HexToColor(textColorHex);
            progressBar.BackColor = HexToColor(buttonColorHex);

            progressBar.ForeColor = HexToColor(progressBarColorHex);

            lblStatus.Location = new System.Drawing.Point(150, 160);
            lblStatus.Size = new System.Drawing.Size(100, 20);
            lblStatus.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;

            cmbOptions.Location = new System.Drawing.Point(30, 30);
            cmbOptions.Width = 340;
            cmbOptions.DropDownStyle = ComboBoxStyle.DropDownList;

            cmbOptions.Items.AddRange(new object[] { "Zipper", "Unzip", "MP3", "MP4" });
            cmbOptions.SelectedIndex = 0;

            txtFilePath.Location = new System.Drawing.Point(30, 60);
            txtFilePath.Width = 340;

            btnExecute.Location = new System.Drawing.Point(150, 90);
            btnExecute.Text = "Execute";
            btnExecute.Width = 100;

            btnExecute.Click += new EventHandler(btnExecute_Click);

            progressBar.Location = new System.Drawing.Point(30, 120);
            progressBar.Width = 340;
            progressBar.Visible = false;

            btnExecute.FlatStyle = FlatStyle.Flat;
            btnExecute.FlatAppearance.BorderSize = 1;
            btnExecute.FlatAppearance.BorderColor = HexToColor(buttonBorderColorHex);

            this.Controls.Add(lblStatus);
            this.Controls.Add(cmbOptions);
            this.Controls.Add(txtFilePath);
            this.Controls.Add(btnExecute);
            this.Controls.Add(progressBar);
        }

        private Color HexToColor(string hex)
        {
            if (hex.StartsWith("#"))
            {
                hex = hex.Substring(1);
            }

            if (hex.Length == 6)
            {
                int r = int.Parse(hex.Substring(0, 2), System.Globalization.NumberStyles.HexNumber);
                int g = int.Parse(hex.Substring(2, 2), System.Globalization.NumberStyles.HexNumber);
                int b = int.Parse(hex.Substring(4, 2), System.Globalization.NumberStyles.HexNumber);

                return Color.FromArgb(r, g, b);
            }
            else
            {
                throw new ArgumentException("Invalid hex string.", nameof(hex));
            }
        }

        private async void btnExecute_Click(object sender, EventArgs e)
        {
            lblStatus.Text = "Processing...";

            try
            {
                string option = cmbOptions.SelectedItem.ToString();
                string inputText = txtFilePath.Text.Trim();

                if (string.IsNullOrEmpty(inputText))
                {
                    MessageBox.Show("Please provide a valid input.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    lblStatus.Text = string.Empty;
                    return;
                }

                progressBar.Visible = true;
                progressBar.Value = 0;

                if (option == "Zipper")
                {
                    string filePath = txtFilePath.Text;
                    bool dirExists = Directory.Exists(filePath);

                    if (dirExists)
                    {
                        string zipFileName = Path.GetFileName(filePath) + ".zip"; // Use original file name for zip
                        string zipFile = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), zipFileName);
                        ZipFile.CreateFromDirectory(filePath, zipFile);
                        MessageBox.Show("Folder zipped successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    else
                    {
                        MessageBox.Show("Invalid directory path.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                else if (option == "Unzip")
                {
                    string zipFile = txtFilePath.Text;
                    bool fileExists = File.Exists(zipFile);

                    if (fileExists)
                    {
                        string extractPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "ExtractedFiles");
                        ZipFile.ExtractToDirectory(zipFile, extractPath);

                        string zipFileName = Path.GetFileNameWithoutExtension(zipFile);
                        string folderPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "ExtractedFiles", zipFileName);

                        MessageBox.Show("File unzipped successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    else
                    {
                        MessageBox.Show("Invalid file path.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                else if (option == "MP3")
                {
                    var video = await YouTube.Default.GetVideoAsync(inputText);

                    string videoName = video.Title; // Retrieve the video name
                    string ext = ".mp3";
                    string outputFilePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), videoName + ext);

                    await Task.Run(() => ConvertToMp3(inputText, outputFilePath));

                    MessageBox.Show("Video converted to MP3 successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else if (option == "MP4")
                {
                    var video = await YouTube.Default.GetVideoAsync(inputText);

                    string videoName = video.Title; // Retrieve the video name
                    string ext = ".mp4";
                    string outputFilePath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), videoName + ext);

                    await Task.Run(() => DownloadVideoWithProgress(video, outputFilePath));

                    MessageBox.Show("Video downloaded as MP4 successfully.", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
                else
                {
                    MessageBox.Show("Invalid option.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                progressBar.Visible = false;
            }

            lblStatus.Text = string.Empty;
        }

        private void ConvertToMp3(string videoUrl, string outputFilePath)
        {
            try
            {
                var youTube = YouTube.Default;
                var video = youTube.GetVideo(videoUrl);

                string tempVideoPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "tempVideo.mp4");
                File.WriteAllBytes(tempVideoPath, video.GetBytes());

                using (var reader = new MediaFoundationReader(tempVideoPath))
                {
                    WaveFileWriter.CreateWaveFile(outputFilePath, reader);
                }

                File.Delete(tempVideoPath);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void DownloadVideoWithProgress(Video video, string outputFilePath)
        {
            byte[] videoBytes = video.GetBytes();
            int totalChunks = videoBytes.Length;

            using (var fileStream = new FileStream(outputFilePath, FileMode.Create))
            {
                byte[] buffer = new byte[8192];
                int bytesRead;
                int totalRead = 0;

                using (var videoStream = video.Stream())
                {
                    while ((bytesRead = videoStream.Read(buffer, 0, buffer.Length)) > 0)
                    {
                        fileStream.Write(buffer, 0, bytesRead);

                        totalRead += bytesRead;
                        int progress = (int)(totalRead * 100.0 / totalChunks);
                        progressBar.Invoke(new Action(() => progressBar.Value = progress));
                    }
                }
            }
        }

        static void Main()
        {
            Application.Run(new Program());
        }
    }
}
