#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_NAME_LEN 50
#define MAX_EMAIL_LEN 100
#define MAX_PHONE_LEN 20
#define MAX_ADDRESS_LEN 200
#define MAX_SCHOOL_LEN 100
#define MAX_COMPANY_LEN 100
#define MAX_TITLE_LEN 100
#define MAX_DESC_LEN 500
#define MAX_ENTRIES 20

// 数据结构定义
typedef struct {
    int id;
    char name[MAX_NAME_LEN];
    char email[MAX_EMAIL_LEN];
    char phone[MAX_PHONE_LEN];
    char address[MAX_ADDRESS_LEN];
    char linkedin[MAX_EMAIL_LEN];
    char github[MAX_EMAIL_LEN];
    time_t created_at;
    time_t updated_at;
} UserBasicInfo;

typedef struct {
    int id;
    int user_id;
    char school[MAX_SCHOOL_LEN];
    char degree[MAX_TITLE_LEN];
    char major[MAX_TITLE_LEN];
    char start_date[11]; // YYYY-MM-DD
    char end_date[11];   // YYYY-MM-DD
    float gpa;
    char description[MAX_DESC_LEN];
} Education;

typedef struct {
    int id;
    int user_id;
    char company[MAX_COMPANY_LEN];
    char position[MAX_TITLE_LEN];
    char start_date[11];
    char end_date[11];
    int is_current;
    char description[MAX_DESC_LEN];
} WorkExperience;

typedef struct {
    int id;
    int user_id;
    char skill_name[MAX_TITLE_LEN];
    char proficiency[20]; // 初级/中级/高级/专家
    char category[50];    // 编程语言/框架/工具等
} Skill;

typedef struct {
    int id;
    int user_id;
    char project_name[MAX_TITLE_LEN];
    char project_url[MAX_EMAIL_LEN];
    char start_date[11];
    char end_date[11];
    char description[MAX_DESC_LEN];
    char technologies[MAX_DESC_LEN];
} Project;

typedef struct {
    UserBasicInfo basic_info;
    Education educations[MAX_ENTRIES];
    WorkExperience experiences[MAX_ENTRIES];
    Skill skills[MAX_ENTRIES];
    Project projects[MAX_ENTRIES];
    int education_count;
    int experience_count;
    int skill_count;
    int project_count;
} Resume;

// 数据库文件管理
void init_database() {
    FILE *file;
    
    // 创建数据目录
    system("mkdir -p resume_data");
    
    // 创建基本表结构文件（这里简化为一个总的数据文件）
    file = fopen("resume_data/resumes.dat", "ab+");
    if (file) fclose(file);
    
    printf("数据库初始化完成\n");
}

// 用户基本信息操作
void save_basic_info(UserBasicInfo *info) {
    FILE *file = fopen("resume_data/basic_info.dat", "ab");
    if (!file) {
        printf("无法打开文件\n");
        return;
    }
    fwrite(info, sizeof(UserBasicInfo), 1, file);
    fclose(file);
}

UserBasicInfo* load_basic_info(int user_id) {
    FILE *file = fopen("resume_data/basic_info.dat", "rb");
    if (!file) return NULL;
    
    static UserBasicInfo info;
    while (fread(&info, sizeof(UserBasicInfo), 1, file)) {
        if (info.id == user_id) {
            fclose(file);
            return &info;
        }
    }
    fclose(file);
    return NULL;
}

// 教育经历操作
void save_education(Education *edu) {
    FILE *file = fopen("resume_data/education.dat", "ab");
    if (!file) return;
    fwrite(edu, sizeof(Education), 1, file);
    fclose(file);
}

int load_educations(int user_id, Education *educations) {
    FILE *file = fopen("resume_data/education.dat", "rb");
    if (!file) return 0;
    
    Education edu;
    int count = 0;
    while (fread(&edu, sizeof(Education), 1, file) && count < MAX_ENTRIES) {
        if (edu.user_id == user_id) {
            educations[count++] = edu;
        }
    }
    fclose(file);
    return count;
}

// 工作经历操作
void save_experience(WorkExperience *exp) {
    FILE *file = fopen("resume_data/experience.dat", "ab");
    if (!file) return;
    fwrite(exp, sizeof(WorkExperience), 1, file);
    fclose(file);
}

int load_experiences(int user_id, WorkExperience *experiences) {
    FILE *file = fopen("resume_data/experience.dat", "rb");
    if (!file) return 0;
    
    WorkExperience exp;
    int count = 0;
    while (fread(&exp, sizeof(WorkExperience), 1, file) && count < MAX_ENTRIES) {
        if (exp.user_id == user_id) {
            experiences[count++] = exp;
        }
    }
    fclose(file);
    return count;
}

// 技能操作
void save_skill(Skill *skill) {
    FILE *file = fopen("resume_data/skills.dat", "ab");
    if (!file) return;
    fwrite(skill, sizeof(Skill), 1, file);
    fclose(file);
}

int load_skills(int user_id, Skill *skills) {
    FILE *file = fopen("resume_data/skills.dat", "rb");
    if (!file) return 0;
    
    Skill skill;
    int count = 0;
    while (fread(&skill, sizeof(Skill), 1, file) && count < MAX_ENTRIES) {
        if (skill.user_id == user_id) {
            skills[count++] = skill;
        }
    }
    fclose(file);
    return count;
}

// 项目经验操作
void save_project(Project *project) {
    FILE *file = fopen("resume_data/projects.dat", "ab");
    if (!file) return;
    fwrite(project, sizeof(Project), 1, file);
    fclose(file);
}

int load_projects(int user_id, Project *projects) {
    FILE *file = fopen("resume_data/projects.dat", "rb");
    if (!file) return 0;
    
    Project project;
    int count = 0;
    while (fread(&project, sizeof(Project), 1, file) && count < MAX_ENTRIES) {
        if (project.user_id == user_id) {
            projects[count++] = project;
        }
    }
    fclose(file);
    return count;
}

// 完整的简历操作
void save_resume(Resume *resume) {
    // 保存基本信息
    resume->basic_info.updated_at = time(NULL);
    save_basic_info(&resume->basic_info);
    
    // 保存教育经历
    for (int i = 0; i < resume->education_count; i++) {
        save_education(&resume->educations[i]);
    }
    
    // 保存工作经历
    for (int i = 0; i < resume->experience_count; i++) {
        save_experience(&resume->experiences[i]);
    }
    
    // 保存技能
    for (int i = 0; i < resume->skill_count; i++) {
        save_skill(&resume->skills[i]);
    }
    
    // 保存项目
    for (int i = 0; i < resume->project_count; i++) {
        save_project(&resume->projects[i]);
    }
}

Resume* load_resume(int user_id) {
    static Resume resume;
    
    // 加载基本信息
    UserBasicInfo *basic_info = load_basic_info(user_id);
    if (!basic_info) return NULL;
    resume.basic_info = *basic_info;
    
    // 加载教育经历
    resume.education_count = load_educations(user_id, resume.educations);
    
    // 加载工作经历
    resume.experience_count = load_experiences(user_id, resume.experiences);
    
    // 加载技能
    resume.skill_count = load_skills(user_id, resume.skills);
    
    // 加载项目
    resume.project_count = load_projects(user_id, resume.projects);
    
    return &resume;
}

// 工具函数
void print_resume(Resume *resume) {
    printf("\n=== 简历信息 ===\n");
    printf("姓名: %s\n", resume->basic_info.name);
    printf("邮箱: %s\n", resume->basic_info.email);
    printf("电话: %s\n", resume->basic_info.phone);
    
    printf("\n教育经历:\n");
    for (int i = 0; i < resume->education_count; i++) {
        printf("- %s | %s | %s - %s\n", 
               resume->educations[i].school,
               resume->educations[i].degree,
               resume->educations[i].start_date,
               resume->educations[i].end_date);
    }
    
    printf("\n工作经历:\n");
    for (int i = 0; i < resume->experience_count; i++) {
        printf("- %s | %s | %s - %s\n", 
               resume->experiences[i].company,
               resume->experiences[i].position,
               resume->experiences[i].start_date,
               resume->experiences[i].end_date);
    }
    
    printf("\n技能:\n");
    for (int i = 0; i < resume->skill_count; i++) {
        printf("- %s (%s)\n", 
               resume->skills[i].skill_name,
               resume->skills[i].proficiency);
    }
}

// 示例使用
int main() {
    init_database();
    
    // 创建示例简历
    Resume resume;
    resume.basic_info.id = 1;
    strcpy(resume.basic_info.name, "张三");
    strcpy(resume.basic_info.email, "zhangsan@email.com");
    strcpy(resume.basic_info.phone, "13800138000");
    resume.basic_info.created_at = time(NULL);
    
    // 添加教育经历
    resume.education_count = 1;
    resume.educations[0].id = 1;
    resume.educations[0].user_id = 1;
    strcpy(resume.educations[0].school, "清华大学");
    strcpy(resume.educations[0].degree, "本科");
    strcpy(resume.educations[0].major, "计算机科学");
    strcpy(resume.educations[0].start_date, "2018-09-01");
    strcpy(resume.educations[0].end_date, "2022-06-30");
    resume.educations[0].gpa = 3.8;
    
    // 保存简历
    save_resume(&resume);
    printf("简历保存成功\n");
    
    // 加载简历
    Resume *loaded_resume = load_resume(1);
    if (loaded_resume) {
        print_resume(loaded_resume);
    }
    
    return 0;
}